# 1. Overview

1. JIRA's comment-update event triggers a webhook to POST comment data to a configured URL.
1. Apache listens on that URL, parses the event data then POSTs it on to a configured Slack
webhook URL.
1. A configured Slack Incoming WebHook receives the JSON data from Flask and posts a comment in
the configured Slack channel.

# 2. Environment

## 1. Create Slack Incoming Webhooks info
- From the dropdown menu for your team, choose **Customize Slack**. Then from the hamburger menu choose
**Configure Apps**. Choose **Build your own** at the top right, and then under **Something just for my team**
choose **Make a Custom Integration**.

- On the **Build a Custom Integration Page** choose **Incoming Webhooks**. You can then either choose an
existing channel, or create a new channel to which messages should be posted. Click the 
**Add Incoming WebHooks Integration** button.

- Scroll further down the new page and you will see some additonal settings that you can make, although no
  further changes are necessary for the integration to work. **Copy the URL** so you can configure
  the server settings later.
  
## 2. API Server Configuration

Clone this repo and update your apache2 settings (/etc/apache2/sites-enabled/) and add a new WSGIAlias to your vhost. An example vhost configuration is supplied in 000-default.conf

Restart Apache

Copy slackcomments.wsgi to your WSGI scripts folder

Edit the slackcomments.wsgi putting in your slack information as well as a user to query the JIRA instance for more information. 

There are a couple of settings you may want to tweak to suit your own environment.

You can change the slack_post variable to False at any point if you do not want it to post to Slack if it meets certain criteria.

# 3. JIRA Webhook Settings

You must go through the standard JIRA webhook creation. Log in as an administrator and type "g+g webhook"

# 4. Documentation / Links

* Slack Attachments --
  https://api.slack.com/docs/attachments

* JIRA Webhook --
  https://developer.atlassian.com/jiradev/jira-apis/webhooks
