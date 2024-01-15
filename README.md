# Monitor the security posture of your IoT application using AWS IoT Device Defender and Splunk #

## Overview ##

Growing adoption of Internet of Things (IoT) applications in regulated industries such as healthcare has necessitated the requirement to secure IoT devices at unprecedented scale. In addition to ensuring that the backend systems required to deliver such critical national services are resilient, organisations are increasingly investing their resources into securing devices that are outside of their traditional enterprise perimeter, using zero trust principles. For example, operators of a fleet of connected medical devices will need to ensure that the product is not exhibiting anomalous behavior, and that they are functioning as designed. In the event a device’s security posture is compromised, it is vital that these events are holistically curated, analyzed and managed by the organization’s centralised security team to continue to safeguard the end-to-end delivery of patient care.

AWS IoT Device Defender is a fully managed IoT security service that enables customers to secure their IoT applications by analyzing device-side and cloud-side metrics in near real-time. Using the export metrics feature, device-side metrics such as the number of bytes of packets sent, and cloud-side metrics such as the number of authorization failures, can be uploaded to a purpose-built enterprise security platform for downstream processing and analysis. 

AWS Partner Splunk provides an analytics-driven security information and event management (SIEM) solution, Splunk Platform, which enables organizations to detect and respond to incidents in real-time. Using Splunk, customers can continue to maintain the security posture of their entire technology estate, from connected devices to workloads in the cloud.

This solution demonstrates how you can use AWS IoT Device Defender, Amazon Kinesis Data Firehose and Splunk’s HTTP Event Collector (HEC) to ingest security-related metrics from IoT devices into Splunk. We will also demonstrate how Splunk can then be leveraged to quickly identify risks and systematically measure the impact from them materializing.

## AWS Blog post ##

This approach is fully documented in the following blog post:

`TBC`

## Deployment ##

### Deploying the solution ###
An [AWS SAM](https://aws.amazon.com/serverless/sam/) template has been provided to deploy all AWS resources required by this solution, including the Python code used by the Lambda function.

A Raspberry Pi running the [Raspberry Pi OS (64-bit)](https://www.raspberrypi.com/software/) is being used to simulate the IoT device.

#### AWS prerequisites ####
For this walkthrough, you will need the following AWS prerequisites to be in place: 

* An AWS account
* IAM permissions to deploy the AWS resources using AWS Serverless Application Model (AWS SAM)
* Local installation of [AWS SAM Command Line Interface (CLI)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
* If you want to test this solution using your own IoT devices, you will be required to provision them separately using AWS IoT Core. IoT applications running on the devices should leverage the [AWS IoT Device SDK](https://docs.aws.amazon.com/iot/latest/developerguide/iot-sdks.html) or the [AWS IoT Device Client](https://github.com/awslabs/aws-iot-device-client), so that device-side metrics are published automatically using the included AWS IoT Device Defender libraries. If not, this logic would need to be coded into your IoT application.

#### Splunk prerequisites ####

You will also need the following Splunk prerequisites to be in place to ingest the data:
* Splunk deployment (Splunk Enterprise or Splunk Cloud) with [HEC enabled](https://docs.splunk.com/Documentation/AddOns/released/AWS/ConfigureFirehoseOverview)
  * HEC must be accessible via a valid SSL certificate
  * If HEC is deployed behind a load-balancer (for Splunk Enterprise), sticky sessions should be enabled to avoid duplicate messages
* [Splunk Add-on for Amazon Web Services](https://splunkbase.splunk.com/app/1876) (optional, but highly recommended)
  * The Splunk Add-on for Amazon Web Services is a Splunk Add-on which helps preconfigure a large number of out of the box AWS source types. Although AWS IoT Device Defender is not currently one of the out-of-the-box source types, it is still recommended to enable this Splunk Add-on to allow the advanced curation of device data alongside data from AWS resources.
* Splunk index 
  * A Splunk index is a repository of data. You will need a Splunk index so that incoming AWS IoT Device Defender data can be indexed and made searchable.

#### Configuring Splunk ####
##### Setup HEC token for Kinesis Data Firehose #####
1. Login to your Splunk Console and select **Settings**, then **Data inputs**. 

![Configuring a new data input](images/splunk_hec_step_1.png)
Figure 2: Configuring a new data input

2. From the **Data inputs** panel select **+ Add new** from the **HTTP Event Collector** section.

![Add a new HEC data input](images/splunk_hec_step_2.png)
Figure 3: Add a new HEC data input

3. From the **Add Data** screen enter a **Name**, select the **Enable indexer acknowledgement** and select **Next**.

![Select a HEC configuration name](images/splunk_hec_step_3.png)
Figure 4: Select a HEC configuration name

4. From the **Input Settings** screen, select **Structured**, then `aws:firehose:json` as your **Source type**.
5. For **Select Allowed Indexes**, select the index you wish to send the AWS IoT Device Defender data to. Select **Review** when done. In this example, we have chosen an index named `aws_hfb`.

![Select HEC input settings](images/splunk_hec_step_4.png)
Figure 5: Select HEC input settings

6. Review the details and select **Submit** when done. 
7. Once you have successfully created the HEC configuration, you will be able to obtain the **Token Value** from the list of HTTP Event Collector configurations. You will need this value when configuring the Kinesis Data Firehose delivery stream.
 
![View the HEC token value](images/splunk_hec_step_5.png)
Figure 6: View the HEC token value

##### Obtain Splunk HEC URL #####
Depending on your Splunk deployment, the assigned HEC URLs will vary. For most Splunk Cloud deployments, the URL will be in the format `https://http-inputs-firehose-<host>.splunkcloud.com:443`. For more information on Splunk HEC URLs, visit *[Set up and use HTTP Event Collector in Splunk Web](https://docs.splunk.com/Documentation/Splunk/latest/Data/UsetheHTTPEventCollector)*.

You now have the HEC URL and Token Value which are required at the time of the AWS SAM template deployment.

#### Deploying the AWS SAM template ####

An aws-samples [GitHub repository](https://github.com/aws-samples/aws-iot-device-defender-and-splunk/) containing the SAM template and Lambda code has been made available so that you can test this solution yourself.

1. Follow the steps in the [official documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) to install the latest release of the AWS SAM CLI for your operating system.
2. Once successfully installed, run `sam --version` to return the AWS SAM CLI version.

> Note: The AWS SAM CLI requires appropriate permissions to provision resources in the chosen AWS account. Ensure that [access key and secret access keys](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/prerequisites.html) have been created using IAM, and that aws configure has been used to register them locally on your machine.
3. To download all required files to your local machine, run the following command.
`git clone https://github.com/aws-samples/aws-iot-device-defender-and-splunk`
4. Navigate to the sam directory.
`cd sam`
5. Build the SAM application.
`sam build`
6. Deploy the application.
`sam deploy --guided`
7. When prompted, enter the unique details chosen for your environment (you can keep the remainder as defaults). In this example, we have chosen deviceDefenderSplunkDemo as the AWS CloudFormation stack name, and aws_iot_device_defender as the Splunk [source type](https://docs.splunk.com/Splexicon:Sourcetype).

```
Stack Name [sam-app]: <Your CloudFormation stack name>
AWS Region [eu-west-1]: <Your AWS region>
Parameter splunkHECEndpoint []: <Your Splunk HEC endpoint>
Parameter splunkHECToken: <Your Splunk HEC token>
Parameter splunkSourceType [aws_iot_device_defender]: <Your Splunk event source type>
```

![Deploying the SAM template](images/deploying_sam_step_1.png)
Figure 7: Deploying the SAM template

8. Confirm that the `Successfully created/updated stack` message is shown. 

![Confirming successful deployment of SAM template](images/deploying_sam_step_2.png)
Figure 8: Confirming successful deployment of SAM template

9. Note down the name of the AWS IoT thing created. This value is outputted by the CloudFormation stack. In this example, the thing name is `deviceDefenderSplunkDemo-IoT-Thing`.
 
![Noting down the AWS IoT thing name](images/deploying_sam_step_3.png)
Figure 9: Noting down the AWS IoT thing name

You are now ready to test the solution.

### Testing the solution ###
To test the solution, we are going to simulate a healthcare device that has potentially been compromised. In this scenario, the rogue device has been tampered with, and has had an FTP server application (`vsftpd`) installed. As a result, it is now listening on an unexpected network port (TCP/21), and the device remains vulnerable to data exfiltration and unauthorized access.

For purposes of the demonstration, the following steps will be performed on a Raspberry Pi 4 device running the Raspberry Pi OS (64-bit), but the process can be similarly repeated on other operating systems running a supported Linux kernel.

#### Generate and download the AWS IoT certificates and keys ####

1. The CloudFormation template has deployed a device in AWS IoT Core, but certificates are yet to be generated. Navigate to the **AWS IoT console**, **All devices**, then **Things**. Select the thing with the name of your CloudFormation stack, and generate the certificates using the **Create certificate** button. 

![Generating device certificates](images/configure_iot_thing_and_certs_step_1.png)
Figure 10: Generating device certificates

2. Make sure that the device certificate is activated, and that device certificate, public key file, private key file and Amazon root certificate have all been securely downloaded. These will be required on the Raspberry Pi device for authentication and authorization with AWS IoT Core.

![Downloading device certificates](images/configure_iot_thing_and_certs_step_2.png)
Figure 11: Downloading device certificates

3. Click on the certificate ID back in the **AWS IoT console**. Under the **Policies** tab, select the **Attach policies** button and attach to the device policy that has been generated for you by the CloudFormation template. This will ensure that the device has the permissions needed to connect, publish and subscribe to the AWS IoT Device Defender’s reserved MQTT topics.

![Attaching device certificate to policy](images/configure_iot_thing_and_certs_step_3.png)
Figure 12: Attaching device certificate to policy

4. The CloudFormation template has already created an AWS IoT Core thing group which is mapped to the AWS IoT Device Defender security profile. Back on the thing page in the **AWS IoT console**, under the **Thing groups** tab, select the **Add to group** button and add the thing to this thing group.

![Adding thing to thing group](images/configure_iot_thing_and_certs_step_4.png)
Figure 13: Adding thing to thing group

Cloud-side metrics will now start to be generated automatically for the device and ingested into Splunk. 

#### Install and run the AWS IoT Device Defender Agent SDK for Python ####

In order to generate device-side metrics, we will use the [AWS IoT Device Defender Agent SDK for Python](https://github.com/aws-samples/aws-iot-device-defender-agent-sdk-python).

1. Note down the AWS IoT Core endpoint details from the **AWS IoT console**.

![Noting down the AWS IoT Core endpoint](images/configure_iot_thing_and_certs_step_5.png)
Figure 14: Noting down the AWS IoT Core endpoint

2. On the Raspberry Pi, create a directory for certificates called `/certs`, and upload the previously downloaded certificate files using a file manager or a secure copy command supported by your workstation. We have renamed the files `AmazonRootCA1.pem`, `certificate.pem.crt` and `private.pem.key` to simplify this example.

```
cd ~
mkdir certs
```

3. Install the [AWS IoT Python SDK](https://github.com/aws/aws-iot-device-sdk-python) by cloning it from GitHub, and running the installer. The AWS IoT Python SDK is a prerequisite for the AWS IoT Device Defender Agent SDK for Python.

```
git clone https://github.com/aws/aws-iot-device-sdk-python.git
cd aws-iot-device-sdk-python
python setup.py install
```

4. Clone the [AWS IoT Device Defender Agent SDK for Python](https://github.com/aws-samples/aws-iot-device-defender-agent-sdk-python) GitHub repository.

```
cd ..
git clone https://github.com/aws-samples/aws-iot-device-defender-agent-sdk-python.git
5.	Install the AWS IoT Device Defender Agent SDK for Python using the installer.
cd aws-iot-device-defender-agent-sdk-python
pip install AWSIoTDeviceDefenderAgentSDK
```

5. Run the sample agent using the AWS endpoint and `ThingName` details noted down earlier, along with the path to the certificates.

> Note: If you ran the previous steps in different directories, ensure that the relative paths reflect the file locations in your environment.

```
cd ~
python aws-iot-device-defender-agent-sdk-python/AWSIoTDeviceDefenderAgentSDK/agent.py --endpoint <your.custom.endpoint.amazonaws.com> --rootCA certs/AmazonRootCA1.pem --cert certs/certificate.pem.crt --key certs/private.pem.key --format json -i 300 -id <ThingName>
```

7. Confirm that no errors are returned, and that the agent connects successfully to the endpoint, and that it subscribes to the reserved AWS IoT Device Defender reserved MQTT topics and publishes data every 5 minutes.

```
Connecting to <your.custom.endpoint.amazonaws.com> with client ID 'deviceDefenderSplunkDemo-IoT-Thing'...
Subscribed to $aws/things/deviceDefenderSplunkDemo-IoT-Thing/defender/metrics/json/accepted with 1
Subscribed to $aws/things/deviceDefenderSplunkDemo-IoT-Thing/defender/metrics/json/rejected with 1
```

8. Once it has been tested that the agent runs correctly, you can run it as a background process using the `$` operator.

```
python aws-iot-device-defender-agent-sdk-python/AWSIoTDeviceDefenderAgentSDK/agent.py --endpoint <your.custom.endpoint.amazonaws.com> --rootCA certs/AmazonRootCA1.pem --cert certs/certificate.pem.crt --key certs/private.pem.key --format json -i 300 -id <ThingName> &
```

#### Simulate the opening of a network vulnerability ####
1. We will now install an FTP server application – `vsftpd` – on the IoT device to open a new TCP listening port.

```
sudo apt install vsftpd
```

2. Confirm after installation that there is now a new TCP port listening on port 21 by running `netstat`. 

> Note: Some ports are duplicated for both IPv4 and IPv6.

```
netstat -plnt
```

![Displaying open TCP ports on the device](images/netstat_confirm_ports.png)
Figure 15: Displaying open TCP ports on the device

We are now ready to see if we can detect this anomaly in Splunk.
