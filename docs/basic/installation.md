# Installation

- Download the plugin
- Copy the `bountyhunter` directory into `caldera/plugins` and enable the plugin in the Caldera server's configuration (`caldera/conf/<config>.yml`)
- Install requirements: `pip install -r requirements.txt`
- Unzip `caldera/plugins/bountyhunter/payloads/payloads.zip` to `caldera/plugins/bountyhunter/payloads`
- Remember to add the `--build` flag when starting the Caldera server with Bounty Hunter for the first time
- Note: Bounty Hunter works with Caldera v5.0.0 or v4.2.0

## Docker Deployment
- Download the plugin from the GitHub repository
- Copy the `bountyhunter` directory into `caldera/plugins` and enable the plugin in the Caldera server's configuration (`caldera/conf/<config>.yml`)
- Add the following lines to the `caldera/Dockerfile` to install the Bounty Hunter requirements during the docker build process, e.g., at line 77 after the installation of the emu plugins requirements in lines 69-76 
```
WORKDIR /usr/src/app/plugins/bountyhunter
RUN pip3 install -r requirements.txt
```
- Continue the docker build as usual
- Note: When using a Caldera docker image, problems during the web ui login might occur ([see here](https://github.com/mitre/caldera/issues/3002)). To avoid problems, add the `--insecure` flag to the docker entry point (`ENTRYPOINT ["python3", "server.py", "--insecure"]`)
