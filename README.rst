Mpsyt Alexa
===========

This is a flask-ask server which allows you to control mpsyt from an Amazon Echo or Amazon Dot.  There are a few steps that you need to go through to get this running:

1. obtain an Echo or Dot, or equivalent device (eg. `Alexa on BeagleBone`_)
2. create an Amazon developer account and set up a new `music` skill
3. generate SSL certificate and submit it on your Amazon developer account
4. run this flask application on the same computer running mpsyt
5. optionally configure and install provided systemd unit to run application as a service

Some of this guide was borrowed from `here`_.

.. _here: https://developer.amazon.com/blogs/post/Tx14R0IYYGH3SKT/Flask-Ask-A-New-Python-Framework-for-Rapid-Alexa-Skills-Kit-Development
.. _Alexa on Beaglebone: https://github.com/merdahl/AlexaBeagleBone2  

Setting up Amazon account
-------------------------

1. Login to your Amazon developer account and [add a new Alexa skill](https://developer.amazon.com/edw/home.html#/skills/list).
2. Under the **Skill Information** tab, set the skill **Name** and **Invocation Name** to ``music`` in the **Skill Information** tab.
3. Under the **Interaction Model** tab, copy the following to the **Intent Schema** and **Sample Utterances** fields.


**Intent Schema**
   
.. code:: json

   {
       "intents": [
           {
               "intent": "StopIntent"
           },
           {
               "intent": "ResumeIntent"
           },
           {
               "intent": "PauseIntent"
           },
           {
               "intent": "NextIntent"
           },
           {
               "intent": "PlayIntent",
               "slots": [
               {
               "name": "request",
               "type": "AMAZON.LITERAL"
               }
               ]
               },
           {
               "intent": "PlayPlaylistIntent",
               "slots": [
                   {
                   "name": "request",
                   "type": "AMAZON.LITERAL"
                   }
               ]
           }
       ]
   }


**Sample Utterances**

.. code::  text

   StopIntent stop
   StopIntent stop song
   ResumeIntent resume
   ResumeIntent resume song
   PauseIntent pause
   PauseIntent pause song
   NextIntent play next
   NextIntent play next song
   PlayIntent play {xxx|request}
   PlayIntent play {xxx xxx|request}
   PlayIntent play {xxx xxx xxx|request}
   PlayIntent play {xxx xxx xxx xxx|request}
   PlayIntent play {xxx xxx xxx xxx xxx|request}
   PlayIntent play {xxx xxx xxx xxx xxx xxx|request}
   PlayIntent play {xxx xxx xxx xxx xxx xxx xxx|request}
   PlayIntent play {xxx xxx xxx xxx xxx xxx xxx xxx|request}
   PlayIntent play {xxx xxx xxx xxx xxx xxx xxx xxx xxx|request}
   PlayIntent play {xxx xxx xxx xxx xxx xxx xxx xxx xxx xxx|request}
   PlayPlaylistIntent play playlist {xxx|request}
   PlayPlaylistIntent play playlist {xxx xxx|request}
   PlayPlaylistIntent play playlist {xxx xxx xxx|request}
   PlayPlaylistIntent play playlist {xxx xxx xxx xxx|request}
   PlayPlaylistIntent play playlist {xxx xxx xxx xxx xxx|request}
   PlayPlaylistIntent play playlist {xxx xxx xxx xxx xxx xxx|request}
   PlayPlaylistIntent play playlist {xxx xxx xxx xxx xxx xxx xxx|request}
   PlayPlaylistIntent play playlist {xxx xxx xxx xxx xxx xxx xxx xxx|request}
   PlayPlaylistIntent play playlist {xxx xxx xxx xxx xxx xxx xxx xxx xxx|request}
   PlayPlaylistIntent play playlist {xxx xxx xxx xxx xxx xxx xxx xxx xxx xx|request}

4. Under the **Configuration** tab, select the ``HTTPS`` endpoint type and enter a url that resolves to the computer that will be running flask, like ``https://example.com``.

5. Under the **SSL Certificate** tab, select ``I will upload a self-signed certificate`` and copy the contents of your ``cert.pem`` file into the field.  (See the `SSL Certificate Generation` section).

6. Under the **Test** tab, enter ``play money pink floyd`` under the **Enter Utterance** field and hit **Ask music**.  Mpsyt should search for Pink Floyd and select the first item.

SSL Certificate Generation
--------------------------
Amazon requires the webhook server to have an SSL certificate.  So long as the project is for individual use, the certificate can be self-signed.

Edit ``ssl.cnf`` and change the ``DNS.1`` field to your domain, like ``example.com``, as mentioned before.

Run the following command to generate the SSL certificate.

.. code:: bash

   openssl req -new -x509 -days 9999 -key private-key.pem -config ssl.cnf -out cert.pem
