# Monitor the security posture of your IoT application using AWS IoT Device Defender and Splunk #

## Overview ##

Growing adoption of Internet of Things (IoT) applications in regulated industries such as healthcare has necessitated the requirement to secure IoT devices at unprecedented scale. In addition to ensuring that the backend systems required to deliver such critical national services are resilient, organisations are increasingly investing their resources into securing devices that are outside of their traditional enterprise perimeter, using zero trust principles. For example, operators of a fleet of connected medical devices will need to ensure that the product is not exhibiting anomalous behavior, and that they are functioning as designed. In the event a device’s security posture is compromised, it is vital that these events are holistically curated, analyzed and managed by the organization’s centralised security team to continue to safeguard the end-to-end delivery of patient care.

AWS IoT Device Defender is a fully managed IoT security service that enables customers to secure their IoT applications by analyzing device-side and cloud-side metrics in near real-time. Using the export metrics feature, device-side metrics such as the number of bytes of packets sent, and cloud-side metrics such as the number of authorization failures, can be uploaded to a purpose-built enterprise security platform for downstream processing and analysis. 

AWS Partner Splunk provides an analytics-driven security information and event management (SIEM) solution, Splunk Platform, which enables organizations to detect and respond to incidents in real-time. Using Splunk, customers can continue to maintain the security posture of their entire technology estate, from connected devices to workloads in the cloud.

This solution demonstrates how you can use AWS IoT Device Defender, Amazon Kinesis Data Firehose and Splunk’s HTTP Event Collector (HEC) to ingest security-related metrics from IoT devices into Splunk. We will also demonstrate how Splunk can then be leveraged to quickly identify risks and systematically measure the impact from them materializing.

## AWS Blog post ##

This approach is fully documented in the following blog post:

`TBC`


