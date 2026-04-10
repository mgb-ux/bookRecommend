# Book Recomendation Search #
This program uses OpenLibrary's search API in order to respond to a user input and find the books most similar to the user input's book based on subject tags from OpenLibrary. It first searches for the user input, then stores the subjects for that user input. The subjects are then searched for and cross referenced to identify the books most similar to the user input, and returns these books, ranked, with hyperlinks.

## Table of Contents ##
1. Installation
2. Usage 
3. Contributing
4. Licensing
5. References

## 1. Installation ##
1. Clone the repository:
```bash
 git clone https://github.com/mgb-ux/bookRecommend
```
2. Install dependencies:
> Make sure python is installed and up to date
> In a terminal:
```bash
cd project
pip install -r requirements.txt
```
> These ensure Flask and requests can run through the python code to connect to the OpenLibrary Search API.
3. Run:
```bash
py main.py
```
## 2. Usage ##
> All [Python](/project/main.py) code has an explanation for its individual purpose tagged with # above the relevant code.
>> requirements.txt allows the user to download the Flask and requests dependencies at once
>>.gitignore allows github to ignore the cache so stale data is not kept where it's not necessary
>
> If running locally, click on the local server. Enter any book, and get book recommendations back!

## 3. Contributing ##
1. Fork the repository: https://github.com/mgb-ux/bookRecommend

2. Create a new branch: 
`git checkout -b feature-name`.
3. Make your changes.
4. Push your branch: 
`git push origin feature-name`.
5. Create a pull request through github.

## 4. Licensing ##
Copyright 2026 Michelle Garcia-Burgos

This program is free software. This program uses OpenLibrary's API and backend in order to facilitate user requests. Anyone can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation. (Taken from Borges, 2011)

See [GNU General Public License](/project/LICENSE.txt) for more details.

For [HTML](/project/index.html) and [CSS](project/styles.css), (Conrad, 2024), which are adapted from Conrad (2024), follow the MIT License:

MIT License

Copyright (c) 2024 Colin Conrad

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 5. References ##
Borges, F. (2011) README. _Python-Openlibrary-Master._ https://github.com/felipeborges/python-openlibrary

Conrad, C. (2024) REB Trainer.  _Case Study 2._ 

OpenLibrary. (2025). _Search API._ https://openlibrary.org/dev/docs/api/search
