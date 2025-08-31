# Contributing

If you want to contribute to this project feel free to open a PR.

This project uses poetry for package management, so it can be installed with `poetry install`. In order to test the integration locally, you need to setup a config folder and link the `custom_compoents` into it like so:

```
mkdir config
cd config
ln -s ../custom_components custom_components
```

Then you can spin up home assistant with Aarhus Waste from the project root:

```
poetry run hass -c config/
```
