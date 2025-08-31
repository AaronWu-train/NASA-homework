# NTU Network Administration and System Administration (2025 Spring)

This repository contains homework assignments and lab exercises for the Network Administration and System Administration course at National Taiwan University (NTU) for the Spring 2025 semester.

## 📁 Repository Structure

### Homework Assignments (`homework0` - `homework12`)
- **homework0**: System installation and basic setup (Arch Linux installation)
- **homework1**: Merkle tree implementation for directory verification
- **homework2**: Network and system administration fundamentals  
- **homework3**: Network switching and configuration with Packet Tracer
- **homework6**: Web server configuration with Nginx
- **homework9**: LDAP directory service setup and configuration
- **homework11**: Security testing with AFL++ fuzzing framework
- **homework12**: Advanced system administration topics

### Lab Exercises (`lab2`, `lab4` - `lab14`)
- Practical exercises complementing homework assignments
- Hands-on system and network administration tasks

### Miscellaneous (`misc/`)
- Additional course materials, practice problems, and resources
- Final exam and midterm materials

## 🛠️ Prerequisites

### Required Software
- **LaTeX Distribution**: TeX Live (recommended) or MiKTeX
  - `xelatex` with shell-escape support
  - Required packages: `geometry`, `amsmath`, `graphicx`, `xeCJK`, `fancyhdr`, `minted`, etc.
- **Make**: For automated building
- **Additional Tools** (assignment-specific):
  - Cisco Packet Tracer (for networking assignments)
  - Linux virtual machines (VirtualBox, QEMU, or similar)
  - Various system administration tools

### LaTeX Installation

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install texlive-full make
```

#### macOS
```bash
brew install --cask mactex
brew install make
```

#### Windows
- Install [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/)
- Install [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm)

## 🚀 Building Assignments

### Individual Assignment
Each homework directory contains a Makefile for easy building:

```bash
cd homework1
make                # Build PDF report
make clean          # Clean auxiliary files
make distclean      # Clean all generated files
make archive        # Create submission archive
```

### Student ID Configuration
Create a `.env` file in the root directory to set your student ID:

```bash
echo "STUDENT_ID=B12345678" > .env
```

This will be used for generating properly named submission files.

### Common Makefile Targets
- `make` or `make all`: Build the PDF report
- `make clean`: Remove LaTeX auxiliary files
- `make distclean`: Remove all generated files including PDFs
- `make archive`: Create a zip archive for submission (includes student ID)

## 📝 Assignment Overview

### LaTeX Reports
Most assignments include LaTeX source files that generate PDF reports containing:
- Problem analysis and solutions
- Implementation details and code
- Screenshots and diagrams
- References and citations

### Code Components
Some assignments include additional deliverables:
- Shell scripts (e.g., `merkle-dir.sh` in homework1)
- Network configuration files
- System configuration examples

### Submission Format
- PDF reports (auto-named with student ID when using `make archive`)
- Additional files as specified in assignment requirements
- Organized in zip archives for easy submission

## 🔧 Development Workflow

1. **Navigate** to the assignment directory
2. **Edit** the LaTeX source files (`report.tex` or `hw*.tex`)
3. **Build** using `make` to generate PDF
4. **Test** your solutions and verify output
5. **Archive** using `make archive` for submission

## 📚 Course Topics Covered

- **System Administration**: Linux installation, user management, service configuration
- **Network Administration**: Switching, routing, LDAP, web servers
- **Security**: Vulnerability assessment, fuzzing, cryptographic attacks
- **Automation**: Shell scripting, system monitoring, backup strategies
- **Virtualization**: VM setup and management

## 🤝 Academic Integrity

This repository contains educational materials for learning purposes. Please follow your institution's academic integrity policies when using these materials.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

For questions about specific assignments, refer to:
- Course documentation and problem statements (`hw*_problem.pdf`)
- Office hours and course forums
- Assignment-specific README files (if available)
