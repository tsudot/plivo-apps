Dial element for an incoming call on a Plivo DID
----------------------------------------------------------
It is used to dial multiple numbers upon receiving an incoming call
on a Plivo DID. 

The numbers are sent as a comma seperated string as a GET parameters to the path `dial`.

    http://heroku-url.com/dial/?numbers=1234567890,9876543210

The following XML is generated for the same.
    `<Response>
        <Speak>
            Welcome, We are connecting your call
        </Speak>
        <Dial>
            <Number>1234567890</Number>
            <Number>9876543210</Number>
        </Dial>
    </Response>`


