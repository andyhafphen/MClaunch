# MClaunch

MClaunch is a simple and user-friendly launcher for Minecraft that allows users to easily download and manage different versions of the game. It features a graphical user interface (GUI) built with Tkinter and supports configuration through a settings file.

## Features

- Download and install multiple versions of Minecraft.
- Manage game assets and libraries automatically.
- User-friendly GUI for easy navigation and operation.
- Confiuration file support for personalized settings.
- Enhanced error handling and logging for better user experience.

## Requirements

- Python 3.x
- Required Python packages:
  - `requests`
  - `tkinter` (usually included with Python)
  - `zipfile` (usually included with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/MClaunch.git
   cd MClaunch
   ```

2. Install the required packages:
   ```bash
   pip install requests
   ```

3. Run the launcher:
   ```bash
   python main.py
   ```

## Configuration

MClaunch uses a configuration file to manage user settings. You can find the configuration file in the project directory. Here’s an example of the configuration format:

```ini
[runtime]
username = "MClaunch"  # In-game username
uuid = "00000000-0000-0000-0000-000000000000"  # User UUID
accesstoken = "0"  # Access token for authentication
usertype = "mojang"  # User type (e.g., mojang, legacy)

[java]
max_memory = "4G"  # Allocated memory/ram/heap size (Xmx)

[installer]
version = "1.21.1"  # Version of the installer
```

## Usage

1. Launch the application.
2. Enter your Minecraft username and other required settings in the configuration file.
3. Select the version of Minecraft you want to install or play.
4. Click the "Launch" button to start the game.

## Changelog

See the [changelog](https://sntry.cc/MinecraftCLf) for a list of changes and updates.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find bugs, please open an issue or submit a pull request.

1. Fork the repository.
2. Create your feature branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Open a pull request.

## Acknowledgments

- Thanks to the Minecraft community for their support and feedback.
- Special thanks to the developers of the libraries used in this project.
```

### Notes:
- Replace `yourusername` in the clone URL with your actual GitHub username.
- Adjust any sections as necessary to fit your specific project details or preferences.
- Make sure to create a `CHANGELOG.md` and `LICENSE` file if you reference them in the README.
