#!/bin/bash
url="http://localhost:11434/api/chat"
model="llama3.2:3b"
container="$1" # I use a docker container as sandbox for bash command
CURRENT_DIR="/root/color-mixer"

message='[
  {
    "role": "system",
    "content": "You have deep expertise in git and linux cli. The user is going to ask you to help him deal with his git repository, as long as linux problems. Please generate the command based on the requirements the user. After that, give a simple and concise explanation of the command."
  }
]'

tools='[
  {
    "type": "function",
    "function": {
      "name": "Execute_command",
      "description": "Run a bash command.",
      "parameters": {
        "type": "object",
        "properties": {
          "command": {
            "type": "string",
            "description": "The command to be executed. You can cd into dir if you want"
          }
        },
        "required": ["command"]
      }
    }
  }
]'

while true; do
  # Prompt the user for input
  echo -n "Enter your prompt (type 'exit' to quit): "
  read user_input

  if [ "$user_input" == "exit" ]; then
    echo "Bye!"
    curl -s "$url" -d "{
      \"model\": \"$model\",
      \"messages\": [],
      \"keep_alive\": 0
    }"
    break
  fi

  # add the user prompt to messages
  message=$(echo "$message" | jq '. += [{"role": "user", "content": $input}]' --arg input "$user_input")

  endcall=false
  while [ "$endcall" == "false" ]; do # continue until there is no tool calls
    body='{
      "model": "'"$model"'",
      "messages": '"$message"',
      "tools": '"$tools"',
      "stream": false
    }'

    response=$(curl "$url" -H "Content-Type: application/json" -d "$body" 2> /dev/null)

    assistant_message=$(echo "$response" | jq .message)
    message=$(echo "$message" | jq '. += [$input]' --argjson input "$assistant_message")

    endcall=true

    tool_calls=$(echo "$response" | jq -r '.message.tool_calls // []')
    if [ "$tool_calls" != "[]" ]; then
      num_calls=$(echo "$tool_calls" | jq 'length')
      for ((i=0; i<num_calls; i++)); do
        command=$(echo "$tool_calls" | jq -r ".[${i}].function.arguments.command")

        echo "[ COMMAND ]"
        echo "$command"

        command_return=$(docker exec -w "$CURRENT_DIR" -it "$container" bash -lc "$command")

        echo "[ COMMAND OUTPUT ]"
        echo "$command_return"
        message=$(echo "$message" | jq '. += [{"role": "tool", "content": $input}]' --arg input "$command_return") # add tool return to messages

        endcall=false #POST again to return command output
      done
    fi

    content=$(echo "$assistant_message" | jq -r '.content // ""') # If message is present, print to the user.
    if [ -n "$content" ]; then
      echo "$content"
    fi
  done
done

