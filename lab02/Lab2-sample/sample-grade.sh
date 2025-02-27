#!/usr/bin/env pwsh
param (
 [string]$script=""
 )
function Test-ExecutePermission {
    param (
        [string]$path
    )
    $permissions = (Get-ChildItem $path).UnixMode
    return $permissions -match "rwx" -or $permissions -match "r-x"
}
if ($script -eq "") {
	Write-Host "Usage: ./sample-grade.sh [your script path]
	(Add ./ if needed)"
}
else{
	if ( -not ( Test-Path -Path $script ) ){
		Write-Output "Your script Does not Exist...?"
		return
	}
	if ( -not ( Test-ExecutePermission -path $script ) ){
		Write-Output "Your script is not executable !!!"
		return
	}

	& $script --input testcase1/test.html --output output.html
	if ( -not ( Test-Path -Path output.html ) ){
		Write-Output "WA :("
		Write-Output "Output file Does not Exist..."
		return
	}
	$objects = @{
  ReferenceObject = (Get-Content -Path testcase1.html)
  DifferenceObject = (Get-Content -Path output.html)
	}
	$result = (Compare-Object @objects)
	if ( $result.count -eq 0 ){
		Write-Output "AC :D"
	}
	else{
		Write-Output "WA :("
		Write-Host $result
	}
	Remove-Item -Path output.html
}
