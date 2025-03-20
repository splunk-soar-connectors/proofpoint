# Proofpoint TAP

Publisher: Splunk Community \
Connector Version: 2.1.0 \
Product Vendor: Proofpoint \
Product Name: Targeted Attack Protection \
Minimum Product Version: 5.5.0

This App integrates with Proofpoint to implement ingestion and investigative actions

### Configuration variables

This table lists the configuration variables required to operate Proofpoint TAP. These variables are specified when configuring a Targeted Attack Protection asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**username** | required | string | Service Principal |
**password** | required | password | Secret |
**initial_ingestion_window** | required | numeric | How far back to search (in minutes) for first poll (maximum 60) |
**ingest_permitted_clicks** | optional | boolean | Ingest Permitted Clicks |
**ingest_blocked_clicks** | optional | boolean | Ingest Blocked Clicks |
**ingest_delivered_messages** | optional | boolean | Ingest Delivered Messages |
**ingest_blocked_messages** | optional | boolean | Ingest Blocked Messages |

### Supported Actions

[test connectivity](#action-test-connectivity) - This action runs a quick query on the server to check the connection and credentials \
[on poll](#action-on-poll) - Callback action for the On Poll ingest functionality \
[get campaign data](#action-get-campaign-data) - Fetch detailed information for a given campaign (deprecated) \
[get campaign](#action-get-campaign) - Fetch detailed information for a given campaign \
[get forensic data](#action-get-forensic-data) - Fetch forensic information for a given threat or campaign (deprecated) \
[get forensic](#action-get-forensic) - Fetch forensic information for a given threat or campaign \
[decode url](#action-decode-url) - Decode Proofpoint rewritten URL(s)

## action: 'test connectivity'

This action runs a quick query on the server to check the connection and credentials

Type: **test** \
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'on poll'

Callback action for the On Poll ingest functionality

Type: **ingest** \
Read only: **True**

For the 'start_time' parameter, the default is the past 10 days and for the 'end_time' parameter, the default is now.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**start_time** | optional | Start of time range, in epoch time (milliseconds) (default is past 10 days) | numeric | |
**end_time** | optional | End of time range, in epoch time (milliseconds) (default is now) | numeric | |
**container_id** | optional | Matching email subject. Wildcards supported | string | |
**container_count** | required | Maximum number of container records to query for | numeric | |
**artifact_count** | required | Maximum number of artifact records to query for | numeric | |

#### Action Output

No Output

## action: 'get campaign data'

Fetch detailed information for a given campaign (deprecated)

Type: **investigate** \
Read only: **True**

This action is deprecated due to action name change. Please use <b>get campaign</b> instead.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**campaign_id** | required | Proofpoint campaign ID from other Proofpoint events | string | `proofpoint campaign id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.campaign_id | string | `proofpoint campaign id` | |
action_result.data.\*.actors.\*.id | string | | |
action_result.data.\*.actors.\*.name | string | | |
action_result.data.\*.campaignMembers.\*.id | string | `proofpoint threat id` | |
action_result.data.\*.campaignMembers.\*.subType | string | | |
action_result.data.\*.campaignMembers.\*.threat | string | | |
action_result.data.\*.campaignMembers.\*.threatTime | string | | |
action_result.data.\*.campaignMembers.\*.type | string | | |
action_result.data.\*.description | string | | |
action_result.data.\*.families.\*.id | string | | |
action_result.data.\*.families.\*.name | string | | |
action_result.data.\*.malware.\*.id | string | | |
action_result.data.\*.malware.\*.name | string | | |
action_result.data.\*.name | string | | |
action_result.data.\*.startDate | string | | |
action_result.data.\*.techniques.\*.id | string | | |
action_result.data.\*.techniques.\*.name | string | | |
action_result.status | string | | success failed |
action_result.message | string | | |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get campaign'

Fetch detailed information for a given campaign

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**campaign_id** | required | Proofpoint campaign ID from other Proofpoint events | string | `proofpoint campaign id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.campaign_id | string | `proofpoint campaign id` | |
action_result.data.\*.actors.\*.id | string | | |
action_result.data.\*.actors.\*.name | string | | |
action_result.data.\*.campaignMembers.\*.id | string | `proofpoint threat id` | |
action_result.data.\*.campaignMembers.\*.subType | string | | |
action_result.data.\*.campaignMembers.\*.threat | string | | |
action_result.data.\*.campaignMembers.\*.threatTime | string | | |
action_result.data.\*.campaignMembers.\*.type | string | | |
action_result.data.\*.description | string | | |
action_result.data.\*.families.\*.id | string | | |
action_result.data.\*.families.\*.name | string | | |
action_result.data.\*.malware.\*.id | string | | |
action_result.data.\*.malware.\*.name | string | | |
action_result.data.\*.name | string | | |
action_result.data.\*.startDate | string | | |
action_result.data.\*.techniques.\*.id | string | | |
action_result.data.\*.techniques.\*.name | string | | |
action_result.status | string | | success failed |
action_result.message | string | | |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get forensic data'

Fetch forensic information for a given threat or campaign (deprecated)

Type: **investigate** \
Read only: **True**

This action is deprecated due to action name change. Please use <b>get forensic</b> instead.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**campaign_id** | optional | Proofpoint campaign ID from other Proofpoint events | string | `proofpoint campaign id` |
**threat_id** | optional | Proofpoint threat ID from other Proofpoint events | string | `proofpoint threat id` |
**include_campaign_forensics** | optional | Include full campaign forensic data for a threat. This value is ignored for campaign queries | boolean | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.campaign_id | string | `proofpoint campaign id` | |
action_result.parameter.include_campaign_forensics | boolean | | |
action_result.parameter.threat_id | string | `proofpoint threat id` | |
action_result.data.\*.generated | string | | |
action_result.data.\*.reports.\*.forensics.\*.display | string | | |
action_result.data.\*.reports.\*.forensics.\*.malicious | string | | |
action_result.data.\*.reports.\*.forensics.\*.platforms.\*.name | string | | |
action_result.data.\*.reports.\*.forensics.\*.platforms.\*.os | string | | |
action_result.data.\*.reports.\*.forensics.\*.platforms.\*.version | string | | |
action_result.data.\*.reports.\*.forensics.\*.time | string | | |
action_result.data.\*.reports.\*.forensics.\*.type | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.action | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.blacklisted | numeric | | |
action_result.data.\*.reports.\*.forensics.\*.what.cnames.\* | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.domain | string | `domain` | |
action_result.data.\*.reports.\*.forensics.\*.what.host | string | `host name` | |
action_result.data.\*.reports.\*.forensics.\*.what.httpStatus | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.ip | string | `ip` | |
action_result.data.\*.reports.\*.forensics.\*.what.ips.\* | string | `ip` | |
action_result.data.\*.reports.\*.forensics.\*.what.key | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.md5 | string | `md5` | |
action_result.data.\*.reports.\*.forensics.\*.what.name | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.nameservers.\* | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.nameserversList.\* | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.offset | numeric | | |
action_result.data.\*.reports.\*.forensics.\*.what.path | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.port | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.rule | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.sha256 | string | `sha256` | |
action_result.data.\*.reports.\*.forensics.\*.what.signatureId | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.size | numeric | | |
action_result.data.\*.reports.\*.forensics.\*.what.type | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.url | string | `url` | |
action_result.data.\*.reports.\*.forensics.\*.what.value | string | | |
action_result.data.\*.reports.\*.id | string | | |
action_result.data.\*.reports.\*.name | string | | |
action_result.data.\*.reports.\*.scope | string | | |
action_result.data.\*.reports.\*.type | string | | |
action_result.status | string | | success failed |
action_result.message | string | | |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get forensic'

Fetch forensic information for a given threat or campaign

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**campaign_id** | optional | Proofpoint campaign ID from other Proofpoint events | string | `proofpoint campaign id` |
**threat_id** | optional | Proofpoint threat ID from other Proofpoint events | string | `proofpoint threat id` |
**include_campaign_forensics** | optional | Include full campaign forensic data for a threat. This value is ignored for campaign queries | boolean | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.campaign_id | string | `proofpoint campaign id` | |
action_result.parameter.include_campaign_forensics | boolean | | |
action_result.parameter.threat_id | string | `proofpoint threat id` | |
action_result.data.\*.generated | string | | |
action_result.data.\*.reports.\*.forensics.\*.display | string | | |
action_result.data.\*.reports.\*.forensics.\*.malicious | string | | |
action_result.data.\*.reports.\*.forensics.\*.platforms.\*.name | string | | |
action_result.data.\*.reports.\*.forensics.\*.platforms.\*.os | string | | |
action_result.data.\*.reports.\*.forensics.\*.platforms.\*.version | string | | |
action_result.data.\*.reports.\*.forensics.\*.time | string | | |
action_result.data.\*.reports.\*.forensics.\*.type | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.action | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.blacklisted | numeric | | |
action_result.data.\*.reports.\*.forensics.\*.what.cnames.\* | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.domain | string | `domain` | |
action_result.data.\*.reports.\*.forensics.\*.what.host | string | `host name` | |
action_result.data.\*.reports.\*.forensics.\*.what.httpStatus | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.ip | string | `ip` | |
action_result.data.\*.reports.\*.forensics.\*.what.ips.\* | string | `ip` | |
action_result.data.\*.reports.\*.forensics.\*.what.key | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.md5 | string | `md5` | |
action_result.data.\*.reports.\*.forensics.\*.what.name | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.nameservers.\* | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.nameserversList.\* | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.offset | numeric | | |
action_result.data.\*.reports.\*.forensics.\*.what.path | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.port | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.rule | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.sha256 | string | `sha256` | |
action_result.data.\*.reports.\*.forensics.\*.what.signatureId | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.size | numeric | | |
action_result.data.\*.reports.\*.forensics.\*.what.type | string | | |
action_result.data.\*.reports.\*.forensics.\*.what.url | string | `url` | |
action_result.data.\*.reports.\*.forensics.\*.what.value | string | | |
action_result.data.\*.reports.\*.id | string | | |
action_result.data.\*.reports.\*.name | string | | |
action_result.data.\*.reports.\*.scope | string | | |
action_result.data.\*.reports.\*.type | string | | |
action_result.status | string | | success failed |
action_result.message | string | | |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'decode url'

Decode Proofpoint rewritten URL(s)

Type: **generic** \
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**url** | required | List of URL(s) to decode, comma separated | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.url | string | | |
action_result.data.\*.urls.\*.clusterName | string | | |
action_result.data.\*.urls.\*.decodedUrl | string | `url` | |
action_result.data.\*.urls.\*.encodedUrl | string | `url` | |
action_result.data.\*.urls.\*.error | string | | |
action_result.data.\*.urls.\*.messageGuid | string | | |
action_result.data.\*.urls.\*.recipientEmail | string | | |
action_result.data.\*.urls.\*.success | boolean | | |
action_result.status | string | | success failed |
action_result.message | string | | |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2025 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
