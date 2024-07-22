# ModernSearchEngines Group Project SS24

## Folder/file structure of the repository:
- `static/documents/`: contains title and short preview text for each document/page (Name: `<docID>.json`)
- `static/pictures/`: contains first picture for each page (Name: `<docID>.<fileSuffix>`)
- `frontier.json`: frontier and already seen links so far
- `index.json`: contains the index in JSON-Format in the following form:

```
[{
   "<term1>":[ [docID1, [positions in text it occurs], skipPointer[index to skip to within postinglist, docID at that index]<br/>/ None (if no skip pointer here)], 
                                      [docID2, [positions in text it occurs], skipPointer]
                                            ...
                                      <docIDx, [positions in text it occurs], skipPointer]],
    ...
   "<termN>": [ [docID1, [positions in text it occurs], skipPointer?], 
                                      [docID2, [positions in text it occurs], skipPointer]
                                       ….
                                      <docIDy, [positions in text it occurs], skipPointer]]
  },
   [[URL0, cluster0, length0 (preprocessed doc)], [URL1, cluster1, length1], …, [URLN,clusterN, lengthN]],
   [hashDoc0, hashDoc1,…, hashDocN], 
   <AverageDocumentLength>
]
```

## How to crawl and build the index?

### If you want to start crawling for the first time:
- set the upper number of documents you want to crawl (variable `MAX_DOCS` above the method 'crawl`)
- now you can run all cells until the cell `Crawl, index`
- run `Crawl, index` to start the crawling process

### If you want to Restart and pick up the crawling process from the state before :
- only run the cell `Crawl, index` again

### If you want to reset & start from new:
- run the cell `Reset before crawling`
- run the cell `Crawl, index`

## Clustering 
After you crawled enough run the Cell `Cluster, add additional infos to index` to determine clusters for the documents 
and add the cluster labels and some other missing data (like skip pointers) to the index.

## Interactive User Interface
Before you can run the user interface, please run the cell under `2. query processing` and the first and second code cell of this document once in order to instanciate the neccessary functions.
Run the cell 12 to start Flask and open the given url.  

## Search from text file
Before you can run the user interface, please run the cell under `2. query processing` and the first and second code cell of this document once in order to instanciate the neccessary functions.
Run the first cell under `3. Search result presentation`.
