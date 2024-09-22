# Obico ML Home Assistant Integration
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square)](https://github.com/custom-components/hacs)

HA Integration for [Obico ML REST API server addon](https://github.com/nobodyguy/obico_ml_ha_addon). This integration allows you to turn any HA Camera entity into a source for Obico's AI 3D printing failure detection.

## Installation

1. Install [HACS](https://hacs.xyz/) (Home Assistant Community Store) if you haven't already.
2. Add this repository to HACS as a custom repository:
   - Go to **HACS** > **Integrations**.
   - Click on the three dots in the upper-right corner and select **Custom repositories**.
   - Enter the URL: `https://github.com/nobodyguy/obico_ml_ha_integration`.
   - Choose **Integration** as the category.
3. Search for **Obico ML** in HACS and install the integration.
4. Restart Home Assistant.

Alternatively, you can manually copy the `obico_ml_ha_integration` folder to your `custom_components` directory.

## Configuration

To configure the integration:

1. Go to **Configuration** > **Integrations** in Home Assistant.
2. Click on the **Add Integration** button.
3. Search for **Obico ML** and click on it to configure.
4. Fill in the configuration parameters.

## Issues

If you encounter any issues or have feature requests, please open an issue on the [GitHub repository](https://github.com/username/ha_prusaconnect_webcam_uploader_integration/issues).

## Contributing

Contributions are welcome! Please open a pull request with any changes or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## TODO
* Docs
* Automation blueprints
* Port predictions - https://github.com/TheSpaghettiDetective/obico-server/blob/release/backend/api/octoprint_views.py#L122
* Resize image