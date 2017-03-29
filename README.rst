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


**Interaction Model**
   
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

.. code::
   StopIntent stop
   StopIntent stop playing
   StopIntent stop song
   StopIntent stop music
   StopIntent stop audio

   PlayIntent play {foo|request}
   PlayIntent play {billy joel|request}
   PlayIntent play {one two three|request}
   PlayIntent play {hamburger three four five|request}
   PlayIntent play {jolly bobby ricky phone nugget|request}

   PlayPlaylistIntent play playlist {foo|request}
   PlayPlaylistIntent play playlist {billy joel|request}
   PlayPlaylistIntent play playlist {one two three|request}
   PlayPlaylistIntent play playlist {hamburger three four five|request}
   PlayPlaylistIntent play playlist {jolly bobby ricky phone nugget|request}

   PauseIntent pause
   PauseIntent pause playing
   PauseIntent pause song
   PauseIntent pause music
   PauseIntent pause audio

   ResumeIntent resume
   ResumeIntent resume playing
   ResumeIntent resume song
   ResumeIntent resume music
   ResumeIntent resume audio

   NextIntent next
   NextIntent next song
   NextIntent next song in playlist
   NextIntent skip
   NextIntent skip song
   NextIntent skip to next song


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
