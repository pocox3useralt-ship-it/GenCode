The GenCode project is a mobile-oriented web application framework designed to build, obfuscate, and deploy Bash-based scripts, specifically tailored for environments like Termux or Acode. It uses a Flask backend to provide a graphical interface for generating payloads and managing remote system interactions.
Core Components
 * Launcher (Run.sh): This script initializes the environment by checking for Python, installing dependencies like flask and pyyaml, and starting the main application.
 * Main Engine (M.py): A Python script that serves a web-based dashboard on port 5901.
 * Configuration (config.yaml): Stores the access credentials; the default username and password are both set to "BREH".
 * Session Management: Uses the flask_session directory to store binary data for authenticated users.
Primary Features
The application includes several specialized modules for system testing and automation:
 * Payload Builder: Allows users to select from various logic modules, such as fork_bomb, storage_fill (creating 1GB files), and encrypt (using AES-256-CBC via OpenSSL).
 * Obfuscation: Features an obf_bash helper that encodes scripts into Base64 to hide their raw content from simple inspection.
 * Remote Terminal: Provides a web-based terminal interface that executes arbitrary shell commands on the host device and returns the output.
 * System Diagnostics: A "Leaks" section uses a dump_info module to gather kernel data, storage usage, and network configuration.
Security and Access
 * Authentication: Users must pass an "Access Gate" login screen to reach the dashboard.
 * Execution Environment: The code includes specific logic to handle paths and permissions (using os.chmod) within mobile terminal environments.

   ![Image](https://drive.google.com/uc?export=view&id=1v_7xxtqqBeUsNtAwXWcGbyReXUd0xaPW)




   # WARNING

## EDUCATIONAL PURPOSES ONLY

*This Tool is for educational purposes only.*

*It is not intended for creating or spreading Virus-related content or harmful software.*

*Any misuse of this Tool for malicious activity, including Virus development or distribution, is strictly discouraged.*

*Use this Tool responsibly and ethically.*
