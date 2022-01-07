[comment]: # "Auto-generated SOAR connector documentation"
# Proofpoint TAP

Publisher: Splunk Community  
Connector Version: 1\.2\.23  
Product Vendor: Proofpoint  
Product Name: Targeted Attack Protection  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.9\.39220  

This App integrates with Proofpoint to implement ingestion and investigative actions

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Targeted Attack Protection asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**username** |  required  | string | Service Principal
**password** |  required  | password | Secret
**initial\_ingestion\_window** |  required  | numeric | How far back to search \(in minutes\) for first poll \(maximum 60\)
**ingest\_permitted\_clicks** |  optional  | boolean | Ingest Permitted Clicks
**ingest\_blocked\_clicks** |  optional  | boolean | Ingest Blocked Clicks
**ingest\_delivered\_messages** |  optional  | boolean | Ingest Delivered Messages
**ingest\_blocked\_messages** |  optional  | boolean | Ingest Blocked Messages

### Supported Actions  
[test connectivity](#action-test-connectivity) - This action runs a quick query on the server to check the connection and credentials  
[on poll](#action-on-poll) - Callback action for the On Poll ingest functionality  
[get campaign data](#action-get-campaign-data) - Fetch detailed information for a given campaign \(deprecated\)  
[get campaign](#action-get-campaign) - Fetch detailed information for a given campaign  
[get forensic data](#action-get-forensic-data) - Fetch forensic information for a given threat or campaign \(deprecated\)  
[get forensic](#action-get-forensic) - Fetch forensic information for a given threat or campaign  
[decode url](#action-decode-url) - Decode Proofpoint rewritten URL\(s\)  

## action: 'test connectivity'
This action runs a quick query on the server to check the connection and credentials

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'on poll'
Callback action for the On Poll ingest functionality

Type: **ingest**  
Read only: **True**

For the 'start\_time' parameter, the default is the past 10 days and for the 'end\_time' parameter, the default is now\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**start\_time** |  optional  | Start of time range, in epoch time \(milliseconds\) \(default is past 10 days\) | numeric | 
**end\_time** |  optional  | End of time range, in epoch time \(milliseconds\) \(default is now\) | numeric | 
**container\_id** |  optional  | Matching email subject\. Wildcards supported | string | 
**container\_count** |  required  | Maximum number of container records to query for | numeric | 
**artifact\_count** |  required  | Maximum number of artifact records to query for | numeric | 

#### Action Output
No Output  

## action: 'get campaign data'
Fetch detailed information for a given campaign \(deprecated\)

Type: **investigate**  
Read only: **True**

This action is deprecated due to action name change\. Please use <b>get campaign</b> instead\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**campaign\_id** |  required  | Proofpoint campaign ID from other Proofpoint events | string |  `proofpoint campaign id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.campaign\_id | string |  `proofpoint campaign id` 
action\_result\.data\.\*\.actors\.\*\.id | string | 
action\_result\.data\.\*\.actors\.\*\.name | string | 
action\_result\.data\.\*\.campaignMembers\.\*\.id | string |  `proofpoint threat id` 
action\_result\.data\.\*\.campaignMembers\.\*\.subType | string | 
action\_result\.data\.\*\.campaignMembers\.\*\.threat | string | 
action\_result\.data\.\*\.campaignMembers\.\*\.threatTime | string | 
action\_result\.data\.\*\.campaignMembers\.\*\.type | string | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.families\.\*\.id | string | 
action\_result\.data\.\*\.families\.\*\.name | string | 
action\_result\.data\.\*\.malware\.\*\.id | string | 
action\_result\.data\.\*\.malware\.\*\.name | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.startDate | string | 
action\_result\.data\.\*\.techniques\.\*\.id | string | 
action\_result\.data\.\*\.techniques\.\*\.name | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get campaign'
Fetch detailed information for a given campaign

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**campaign\_id** |  required  | Proofpoint campaign ID from other Proofpoint events | string |  `proofpoint campaign id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.campaign\_id | string |  `proofpoint campaign id` 
action\_result\.data\.\*\.actors\.\*\.id | string | 
action\_result\.data\.\*\.actors\.\*\.name | string | 
action\_result\.data\.\*\.campaignMembers\.\*\.id | string |  `proofpoint threat id` 
action\_result\.data\.\*\.campaignMembers\.\*\.subType | string | 
action\_result\.data\.\*\.campaignMembers\.\*\.threat | string | 
action\_result\.data\.\*\.campaignMembers\.\*\.threatTime | string | 
action\_result\.data\.\*\.campaignMembers\.\*\.type | string | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.families\.\*\.id | string | 
action\_result\.data\.\*\.families\.\*\.name | string | 
action\_result\.data\.\*\.malware\.\*\.id | string | 
action\_result\.data\.\*\.malware\.\*\.name | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.startDate | string | 
action\_result\.data\.\*\.techniques\.\*\.id | string | 
action\_result\.data\.\*\.techniques\.\*\.name | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get forensic data'
Fetch forensic information for a given threat or campaign \(deprecated\)

Type: **investigate**  
Read only: **True**

This action is deprecated due to action name change\. Please use <b>get forensic</b> instead\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**campaign\_id** |  optional  | Proofpoint campaign ID from other Proofpoint events | string |  `proofpoint campaign id` 
**threat\_id** |  optional  | Proofpoint threat ID from other Proofpoint events | string |  `proofpoint threat id` 
**include\_campaign\_forensics** |  optional  | Include full campaign forensic data for a threat\. This value is ignored for campaign queries | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.campaign\_id | string |  `proofpoint campaign id` 
action\_result\.parameter\.include\_campaign\_forensics | boolean | 
action\_result\.parameter\.threat\_id | string |  `proofpoint threat id` 
action\_result\.data\.\*\.generated | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.display | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.malicious | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.platforms\.\*\.name | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.platforms\.\*\.os | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.platforms\.\*\.version | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.time | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.type | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.action | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.blacklisted | numeric | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.cnames\.\* | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.domain | string |  `domain` 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.host | string |  `host name` 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.httpStatus | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.ip | string |  `ip` 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.ips\.\* | string |  `ip` 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.key | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.md5 | string |  `md5` 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.name | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.nameservers\.\* | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.nameserversList\.\* | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.offset | numeric | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.path | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.port | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.rule | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.sha256 | string |  `sha256` 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.signatureId | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.size | numeric | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.type | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.url | string |  `url` 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.value | string | 
action\_result\.data\.\*\.reports\.\*\.id | string | 
action\_result\.data\.\*\.reports\.\*\.name | string | 
action\_result\.data\.\*\.reports\.\*\.scope | string | 
action\_result\.data\.\*\.reports\.\*\.type | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get forensic'
Fetch forensic information for a given threat or campaign

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**campaign\_id** |  optional  | Proofpoint campaign ID from other Proofpoint events | string |  `proofpoint campaign id` 
**threat\_id** |  optional  | Proofpoint threat ID from other Proofpoint events | string |  `proofpoint threat id` 
**include\_campaign\_forensics** |  optional  | Include full campaign forensic data for a threat\. This value is ignored for campaign queries | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.campaign\_id | string |  `proofpoint campaign id` 
action\_result\.parameter\.include\_campaign\_forensics | boolean | 
action\_result\.parameter\.threat\_id | string |  `proofpoint threat id` 
action\_result\.data\.\*\.generated | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.display | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.malicious | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.platforms\.\*\.name | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.platforms\.\*\.os | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.platforms\.\*\.version | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.time | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.type | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.action | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.blacklisted | numeric | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.cnames\.\* | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.domain | string |  `domain` 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.host | string |  `host name` 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.httpStatus | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.ip | string |  `ip` 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.ips\.\* | string |  `ip` 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.key | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.md5 | string |  `md5` 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.name | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.nameservers\.\* | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.nameserversList\.\* | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.offset | numeric | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.path | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.port | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.rule | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.sha256 | string |  `sha256` 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.signatureId | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.size | numeric | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.type | string | 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.url | string |  `url` 
action\_result\.data\.\*\.reports\.\*\.forensics\.\*\.what\.value | string | 
action\_result\.data\.\*\.reports\.\*\.id | string | 
action\_result\.data\.\*\.reports\.\*\.name | string | 
action\_result\.data\.\*\.reports\.\*\.scope | string | 
action\_result\.data\.\*\.reports\.\*\.type | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'decode url'
Decode Proofpoint rewritten URL\(s\)

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**url** |  required  | List of URL\(s\) to decode, comma separated | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.url | string | 
action\_result\.data\.\*\.urls\.\*\.clusterName | string | 
action\_result\.data\.\*\.urls\.\*\.decodedUrl | string |  `url` 
action\_result\.data\.\*\.urls\.\*\.encodedUrl | string |  `url` 
action\_result\.data\.\*\.urls\.\*\.error | string | 
action\_result\.data\.\*\.urls\.\*\.messageGuid | string | 
action\_result\.data\.\*\.urls\.\*\.recipientEmail | string | 
action\_result\.data\.\*\.urls\.\*\.success | boolean | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 