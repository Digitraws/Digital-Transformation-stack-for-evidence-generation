# Digital Transformation stack for evidence generation
In an era dominated by digital content, ensuring its integrity stands as a
critical challenge. This project presents a pioneering solution, safeguarding digital
content against tampering and ensuring its authenticity. By integrating cutting-edge
technologies like cryptographic signatures and blockchain, DigiTraWS fortifies the
trustworthiness of served content. This system not only offers an immutable audit trail
but also fosters confidence and reliability in digital interactions, paving the way for a
more accountable and secure digital landscape.

## UML
![img](flow.svg)


## Plan
### Static Webpage evidence collection.
Here static means devoid of background fetching.

1. Extract the parts which are visible/displayed/rendered.
This will already be there in the browser somewhere (dk where).
2. Link all those requests to their respective locations on the webpage.
Need to check how the browser does it.
3. Finally, store them in some tree format and make evidence. (JSON or similar structure)
4. extract this evidence and display it in the local browser or similar.


#### Things to note.
1. For our evidence to be robust enough, we must store at least the properties (content+timestamp+URL/link (HTTP response), signature).
2. The timestamps of all the objects in a particular evidence must be within a certain timeframe (T secs).
    1. There could be corner cases where the evidence is not truly correct, but the probability of that happening is very unlikely.