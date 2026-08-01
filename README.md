# UofT Course Web
2026-present <br>
Personal project - First Python program without prior Python experience - Made without AI assistance <br>
<br>
Uses: requests, BeautifulSoup4 <br>
<br>
Disclaimer: Please always cross reference the information of University of Toronto's Academic Calendar. The tool may not be 100% perfect and may sometimes misrepresent / misunderstand the data. This tool currently exclusively applies to the St. George campus. 

---
The program functions through scraping UofT's academic calendar get course prerequisites and will be able to represent them visually. <br>
Features (will) include:
- Being able to figure out what course prerequisites are required to take a certain course, including nested prerequisites (For instance, CSC413H1 needs CSC311H1 (as listed) which also needs CSC108H1 which also needs ...)
- Being able to see what courses you could 'unlock' if you take a certain course. (For instance, by taking CSC311H1 you can take CSC413H1)
- Being able to look up the minimum grade requirements, if applicable. 
- Being able to visualize the above using the NetworkX Python package (or something similar).
<br>

---
### Current progress:
- Basic scraper that covers most prerequisite format cases.
<br>

To Do:
- Scrape all course information
- Represent them through NetworkX
<br>

Future further development ideas:
- Have the program automatically check off which specialist/major/minor you could complete with a selection on certain courses
  - Can also display how many more / what courses you need to complete the specialist/major/minor
<br>

---
### Backstory:
I was planning my courses for UofT and I honestly forget why I added MAT224H1 to my plan. Was it a prerequisite for any courses I wanted? Or was it something I did for fun??? Was it for the math specialist? Thus, I thought it would be a good idea to write such a program to fix that and future problems.
