# AMARO BI Case - Data Engineer
======================================

## About the case

You need to create an API for a report system to consult data aggregated for analysis, with the following requisites.

### Request made by the client to your API:
 * __startTimestamp__ : This is a mandatory parameter to the client. It's the inital timestamp from when the client needs the data (in the format of '2017-12-03 13:55:00')
 * __endTimestamp__ : This is a mandatory parameter to the client. It's the final timestamp from when the client needs the data (in the format of '2017-12-04 13:55:00')
 * __aggregation__ : This is a mandatory parameter to the client. It's the interval aggregation that the client needs the data. It's expressed in minutes. It can be for example: 60, if this is the case you should return one value per hour.
 * __product__ : This is an optional parameter. The client may want to filter one specific produtct. This is a string as shown below.
 * __platform__ : This is an optional parameter. The client may want to filter one of the 3 platforms 'iOS', 'Android', 'MobileWeb'

### Response the client is expecting:
 * __timestamp__ : It's the initial timestamp of each aggregation
 * __platform__ : It's the platform as explained above
 * __product__ : It's the product as explained above
 * __CTR__ : This is the metric the client is interested in. It's calculated as the #purchases / #productViews, and the value is expected in the decimal format with four digits [0.0150], which means a CTR of 1.50% (those values are explained below)

## Guidelines
 * Try to use the best practices when programming an API
 * Keep in mind that the system needs to be modular to allow changes and upgrades in the future
 * Create your own repository and when coming to present please share it with AMARO
 * Think about scalability because when dealing with production data, the volume can be very high.
 * Write down the main guidelines to use your system on the Readme file.
