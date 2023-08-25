# Digital Transformation stack for evidence generation

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

## To-Do List 
- [ ] Client side
    - [x] Create a static HTML page and fetch evidence that contains static
    - [x] Images
    - [x] Videos
    - [x] Audio
    - [x] Reconstruct a viewable evidence from the serialzed version
    - [ ] Save the `evidence/` as a compressed file (maybe later)
    - [ ] robustify the custom script
        - [ ] do the testing on various platforms
        - [ ] do testing on iframe websites
        - [ ] note down the limitations
        - [x] make the regex more strong
    - [ ] HAR
        - [ ] viewable content extraction from har
- [ ] Server side
    - [ ] sign `content` + `public_key`
    - [ ] Add custom headers to the server
    - [ ] create multliple servers with this property
- [ ] Create a function to verify the signatures

## Done (but not worked)
- tried `wget` but didn't work
    - beacuse of endless looping having several edge cases
    - link replacing wont work as expected
    - custom script wont work
