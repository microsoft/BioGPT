## BioGPT on Google Cloud Platform using Pulumi

### Requirements

- Python 3
- Pulumi, https://www.pulumi.com/docs/get-started/install/

### Instructions

1. Create a service account in Google Cloud Platform as follows:

	* Log in to the Google Cloud Console (console.cloud.google.com)
	* Select the project in which you want to create a service account
	* Click on the "IAM & Admin" option in the left-hand menu
	* Click on "Service Accounts" in the left-hand menu
	* Click the "Create Service Account" button
	* Enter a name for the service account
	* Select "Editor" role for the service account
	* Select "Furnish a new private key" option and choose JSON
	* Click "Create" to create the service account
	* Once you have created the service account, you will be prompted to download the private key file

2. Rename service account private key file to `gcp.json` and place it inside the `/infra` directory
3. Rename `.sample.env` to `.env` and edit its contents
4. Execute in your terminal `./start.sh` to:

	* Enable Google Cloud Services
	* Build and push a Docker image to Google Container Registry
	* Spin up a Kubernetes cluster running a K80 GPU
	* Install NVIDIA driver into Kubernetes cluster
	* Launch the BioGPT Kubernetes deployment
	* Expose BioGPT to the public internet using a Kubernetes Service

### How to use

Once `./start.sh` finishes running it will output `load_balancer_ip`, for example: `load_balancer_ip: "34.172.48.137"`. Use the IP provided to query BioGPT.

Parameters:
- text (required): The text you want to send as a query to BioGPT
- min_len (optional, default: 100): The minimum length of the generated response
- max_len_b (optional, default: 1024): The maximum length of the generated response
- beam (optional, default: 5)

For example: `http://34.172.48.137:5000/?text=Your_Query_Here&min_len=100&max_len_b=1024&beam=5`. Replace `Your_Query_Here` with your desired query text, and adjust the values for `min_len`, `max_len_b`, and `beam` as needed.

Remember to URL-encode the text parameter if it contains special characters or spaces. For example, you can replace spaces with `%20`.

### Delete cluster and revert all changes

To delete the cluster and revert all changes, execute in your terminal: `./destroy.sh`.

### Support

If you like this project and find it useful, please consider giving it a star. Your support is appreciated! :hearts:

If you have any questions or suggestions, feel free to reach out to Carlos at calufa@gmail.com or connecting on LinkedIn: https://www.linkedin.com/in/carloschinchilla/.
