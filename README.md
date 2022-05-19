# Modzy Integration GitHub Actions

<div align="center">
<img src="https://www.modzy.com/wp-content/uploads/2020/06/MODZY-RGB-POS.png" alt="modzy logo" width="250" align="center"/>
  
**This repository illustrates a CI/CD pipeline to automate the deployment of machine learning models to Modzy.**

![GitHub contributors](https://img.shields.io/github/contributors/modzy/github-action-model-deployment)
![GitHub last commit](https://img.shields.io/github/last-commit/modzy/github-action-model-deployment)
![GitHub Release Date](https://img.shields.io/github/issues-raw/modzy/github-action-model-deployment)

[Chassis](<https://github.com/modzy/chassis>)
</div>

## Overview

The objective of this repository is to provide a reference implementation of a GitHub Actions workflow that gives data scientists a mechanism to train their model(s) in their preferred workspace (e.g., this repository), configure a single JSON file (`model_info.json`), and simply commit their changes to the `main` branch. Doing so will trigger the CI/CD workflow, which will take resources from this repository and execute some [Chassis](https://chassis.ml) python code to automatically containerize and deploy the trained model to Modzy. Please note that the implementation of the GitHub Actions workflow in this repository can be modified and set up several different ways, so this is a great place to start if you are interested in creating your own CI/CD pipeline!

## Repository Contents

The layout of this repository is strictly an example of how a data scientist might construct a model training repository. Feel free to set up your own repository however you wish.

* `.github/`: Folder that contains the GitHub action workflow definition in `workflows/ci.yml`
* `data/`: Folder to hold any training data, sample test data, or additional model dependencies
* `weights/`: Folder to hold any saved model weights
* `train.py`: Python script that trains and saves the weights locally for a scikit-learn logistic regression model
* `model_info.json`: Single JSON file used to define model information. The GitHub action references this file to complete the execution of the CI/CD workflow.  
* `requirements.txt`: Contains list of python packages required to execute any script in this repository

## Usage Instructions

This repository is structured in a way such that data scientists only need to update weights files and `model_info.json` any time they need to update a model. The workflow is set to execute upon every commit to the `main` branch and will automatically execute [Chassis](https://chassis.ml) code to containerize and deploy the model. 

**As a data scientist...**
* Train your model and save your weights file according to your preference (`weights/model_latest.pkl` for example)
* Fill in the following information in `model_info.json`:
    * `name`: Desired name for your model when it is deployed to Modzy
    * `version`: Version of your model to deploy. *Note: You can deploy as many versions of the same model to Modzy as you wish*
    * `weightsFilePath`: File path in this repository to your updated weights file
    * `sampleDataFilePath`: File path in this repository to a sample data file that can be used to test your model during the CI/CD process.

Example `model_info.json`:
```
{
    "name": "GitHub Actions Sklearn Logistic Regression",
    "version": "0.0.1",
    "weightsFilePath": "weights/model_latest.pkl",
    "sampleDataFilePath": "data/digits_sample.json"
}
```

**As a DevOps or machine learning engineer...**
* Ensure the Chassis code in the `.github/workflows/ci.yml` file aligns with the model the data scientist is building. Specifically the `process` method must read in the sample data properly, use the loaded model to make predictions, and return the results in the data scientist's desired format.
* Navigate to the Settings tab within this repository and click on Secrets --> Actions. Set the following Secrets (to be accessed in the GitHub Action workflow):
    * `CHASSIS_SERVICE`: URL to publicly-hosted Chassis service
    * `DOCKER_USER`: Valid Dockerhub username
    * `DOCKER_PASS`: Valid Dockerhub password
    * `MODZY_URL`: Valid Modzy instance URL
    * `MODZY_API_KEY`: Valid Modzy API key associated with `MODZY_URL` instance. *Note: this API key must be associated with a user that has the "Data Scientist" role*.


## Contributing

We are happy to receive contributions from all of our users. Check out our [contributing file](https://github.com/modzy/github-action-model-deployment/blob/master/CONTRIBUTING.adoc) to learn more.

## Code of conduct

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](https://github.com/modzy/github-action-model-deployment/blob/master/CODE_OF_CONDUCT.md)
