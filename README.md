# AMARO BI Case - Data Engineer

## About the case

#### Context:
To attend AMARO's needs, the BI team developed an internal visualization tool that has the front-end and the backend engine as different services. You should develop this backend engine, that will communicate with the front-end and query the data in the different systems we have.

#### Goal:
You need to create an API that will:
 * Receive a request from the front-end (specified below)
 * Query data and transform it 
 * Returning the resuts (also as specified below)

## Part I

### Request made by the client to your API:
 * __startTimestamp__ : This is a mandatory parameter to the client. It's the inital timestamp from when the client needs the data (in the format of '2017-12-03 13:55:00')
 * __endTimestamp__ : This is a mandatory parameter to the client. It's the final timestamp from when the client needs the data (in the format of '2017-12-04 13:55:00')
 * __aggregation__ : This is a mandatory parameter to the client. It's the interval aggregation that the client needs the data. It's expressed in minutes. It can be for example: 60, if this is the case you should return one value per hour.
 * __product__ : This is an optional parameter. The client may want to filter one specific produtct. This is a string as shown below. If the request doesn't send a product parameter you should return one result for each product.
 * __platform__ : This is an optional parameter. The client may want to filter one of the 3 platforms 'iOS', 'Android', 'MobileWeb'. If the request doesn't send the platform, you should return one result for each platform.

### Response the client is expecting:
 * __timestamp__ : It's the initial timestamp of each aggregation
 * __platform__ : It's the platform as explained above
 * __product__ : It's the product as explained above
 * __CTR__ : This is the metric the client is interested in. It's calculated as the #purchases / #productViews, and the value is expected in the decimal format with four digits [0.0150], which means a CTR of 1.50% (those values are explained below)
 
### Internal Specification for your system to query the data and transform it:

To calculate the CTR metric, you will have to join purchase data from SQL Tables (explained below) and productView data from JSONs store on an S3 bucket.

The CTR metric is calculated by the number of 'purchases' divided by the number of events 'productViews' made in a platform for a specific product during the requested period.

#### Getting purchase data
Your system has to get purchase data from the SQL database. We're sending two CSV files, with several columns.

The order table has one record for each transaction made, no matter how many items it was purchased.
The order_items table has one record for each item purchased.
Relationship is: orders 1:N order_items, joined by orders.id = order_items.order_id

The main columns are:
 * __orders.id__ : the id of the order made
 * __orders.order_date__ : the datetime when the order was made
 * __orders.status__ : the status of the order
 * __orders.device__ : the device where the order was placed
 * __orders.order_total__ : the revenue of the order
 * __order_items.order_id__ : the id of the order that this item belongs to
 * __order_items.code_color__ : the id of the product purchased

#### Getting productView data
Your system has to get data from a folder with several JSON files (in production would be an S3, but we're sending a ZIP folder with all JSONs).

The JSON has the following structure:

```
{
"events":
 [
    {
     "data": 
      {
          "custom_event_type":"navigation",
          "event_name":"product",
          "timestamp_unixtime_ms":1515546904352,
          "event_id":679644799952992890,
          "session_id":-7147916473548193691,
          "custom_attributes":  {
            "actualPrice":"189.9",
            "base":"p",
            "codeColor":"20008657_002"
          }
      },
      "event_type":"custom_event"
    }
 ],
 "mpid":-196509116834317511,
 "timestamp_unixtime_ms":1515546904352,
 "batch_id":4541028697219217452,
 "message_id":"67a98f22-cc4d-4e90-a14b-e74899a88da8",
 "message_type":"events",
 "schema_version":1
}
```

This object is an event, of:
 * "event_type":"custom_event"  - we're only interested in those "custom_event", the other types can be ignored
 * "event_name":"product" - the name of this custom_event is "product" 
 * This event has a custom_attribute called "codeColor", this attribute represents the ID of the product, that can be used by the client as a parameter, and it's the same value as the column "order_items.code_color" in the database
 * There's a different folder for each platform, all events inside each folder are exclusive of that platform.

## Guidelines
 * Try to use the best practices when programming an API
 * Keep in mind that the system needs to be modular to allow changes and upgrades in the future
 * Create your own repository and when coming to present please share it with AMARO
 * Think about scalability because when dealing with production data, the volume can be very high.
 * Write down the main guidelines to use your system on the Readme file.

## Part II
