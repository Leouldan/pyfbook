#pyfbook

A python package to easily collect data from Facebook APIs (Marketing,
Page and Graph)

###1) Installation

Open a terminal and install pyfbook package

::

   pip install pyfbook

###2) Configuration

Name your project (ex: your facebook app name).

Add in your environment : - export FB_%s_APP_ID = “YOUR_FACEBOOK_APP_ID”
- export FB_%s_APP_SECRET = “YOUR_FACEBOOK_APP_SECRET” - export
FB_%s_ACCESSTOKEN = “YOUR_FACEBOOK_ACCESSTOKEN”

Replace ‘%s’ with your project name.

###3) Marketing

#####\ *Configuration* Init a yaml file and add its path to your
environment: - export FACEBOOK_MARKETING_%s_YAML_PATH =
“./metric_dimension.yaml”

Or

::

   import os
   os.environ["FACEBOOK_MARKETING_%s_YAML_PATH"]="./metric_dimension.yaml"

This .yaml file must be structured as :

::

   key:
     level: account or campaign or adset or ad
     fields:
     - list of fields
     breakdowns (optional):
     - country or gender etc...
     time_increment:
     - list of time increment you want ('1', all_days etc...)

Please go to
https://developers.facebook.com/docs/marketing-api/advanced-measurement
to have all details.

Below an example of metric_dimension.yaml file:

::

   account:
     level: account
     fields:
     - impressions
     - spend
     - clicks
     - unique_clicks
     - total_actions
     - total_unique_actions
     - reach
     - date_start
     - date_stop
     - account_id
     time_increment:
     - all_days
     - "1"

   campaign:
     level: campaign
     fields:
     - campaign_name
     - impressions
     - spend
     - clicks
     - unique_clicks
     - total_actions
     - total_unique_actions
     - reach
     - objective
     - campaign_id
     - date_start
     - date_stop
     - account_id
     time_increment:
     - all_days
     

#####\ *Connector*

-  project: your project name
-  start: “YYYY-MM-DD”
-  end: “YYYY-MM-DD”
-  all_account_id: list of all account_id you want to get insights from
   (ex: [“act_XXXXX”, “act_XXXXX”])
-  *(optional)* spreadsheet_id **Not developed yet**
-  *(optional)* redshift_instance: see pyred documentation

   get_marketing( project, start, end, all_account_id,
   spreadsheet_id=None, redshift_instance=None, test=False)

###4) Graph

#####\ *Configuration* Init a yaml file and add its path to your
environment: - export FACEBOOK_GRAPH_%s_YAML_PATH =
“./metric_dimension.yaml”

Or

::

   import os
   os.environ["FACEBOOK_GRAPH_%s_YAML_PATH"]="./metric_dimension.yaml"

This .yaml file must be structured as :

::

   key:
     endpoint: an existing endpoint from the graph api
     fields:
     - list of fields
     

#####\ *Connector*

-  project: your project name
-  *(optional)* user_id
-  *(optional)* spreadsheet_id **Not developed yet**
-  *(optional)* redshift_instance: see pyred documentation

::
   get_account_info( project, user_id=“me”,
