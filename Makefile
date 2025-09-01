clean: 
	rm -rf config/
	mkdir config
	
link:
	ln -s "${PWD}/custom_components" "${PWD}/config/custom_components"

reset: clean link

run:
	poetry run hass -c config/
