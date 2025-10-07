# BookShelf

## Introduction

BookShelf is a reading log app for book lovers who want to keep track of their reading. BookShelf helps you record, rate, and review your favourite books. 

**Personalised Reviews:** Log the books you’ve read, write detailed reviews, and rate them.  

**Edit and Manage:** Update or delete your reviews as your thoughts evolve, or on subsequent reads.  

**Discover New Reads:** Browse the homepage to see reviews from other readers to see what they thought of a book, or discover new recommendations.  

**Sort Easily:** Sort reviews by rating, book, or author, to quickly find what you’re looking for.

## Table of Contents

- [Introduction](#introduction)
- [Deployed Site](#deployed-site)
- [Features](#features)
  - [Messages](#messages)
- [Future Features](#future-features)
- [UX](#ux)
  - [Design](#design)
    - [ERD](#erd)
    - [Fonts](#fonts)
    - [Colour Scheme](#colour-scheme)
    - [Wireframes](#wireframes)
    - [Responsivity](#responsivity)
    - [User Stories](#user-stories)
    - [Agile](#agile)
- [Tech Used](#tech-used)
- [Testing](#testing)
  - [Accessibility](#accessibility)
  - [Lighthouse](#lighthouse)
  - [Manual](#manual)
  - [Unit Tests](#unit-tests)
  - [Validation](#validation)
- [AI Use](#ai-use)
- [Deployment](#deployment)
- [Credits](#credits)

## Deployed site

The site was deployed on Heroku:
[BookShelf](https://book-shelf-app-cdf881ab4579.herokuapp.com/)

## Features

### Main Pages
<!-- all review, my bookshelf, review detail (rating stars)-->
<!-- message for no reviews -->
<!-- sorting -->
<!-- header changes -->
### Login/Signup
<!-- pages -->
<!-- login/out indication -->
<!-- messages for login/out -->

<!-- admin access -->
### CRUD Functionaliy
<!-- Add review form, validation, limitations? -->
<!-- edit review, validation -->
<!-- delete review -->
<!-- messages for all -->
### Defensive Programming
<!-- messages & prevention of deletion/edit -->
<!-- attempt to access login pages -->
## Future Features
<!-- reading stats, all reviews for book, author pages, draft reviews -could, filter reviews - could, images for book covers -could , search function, further check for adding book/author -->
<!-- suggest book/author deletion  -->
<!-- QoL - login/out on enter - although can tab -->
## Database Design and ERD
<!-- Rational -->
## UX 
### Design

Overall, for the design I wanted to evoke an old journal, or library. My design choices were made with this in mind.

#### Colour Scheme

| Colour      | Hex Code    |
| ----------- | ----------- |
| Red Leather | #9b2626   |
| Parchment   | #dbc8a4   |
| Bronze/Gold | #b8860b   |
| Ink Blue    | #2f51a2   |
| Wood Brown  | #452819   |


The header/navigation has a dark wood effect image as the background, evoking a book shelf.

The centre section has a red background, with a slight gradient, mimicking the red leather you might find on an old book. 

Down the side, the site has decorative scrollwork on a parchment background - like you might find on old illustrated books.

The review cards have a parchment (off-white) colour to them, with a slight gradient to make it feel more organic. 

The titles for each review are in a dark blue to mimic fountain pen ink. 

Accents, such as buttons or borders, are in a bronze/gold colour such as you might find on journal clasps. Buttons have an inset box-shadow applied in a lighter shade, to make them seem as if they have a shine, and appear more 3D.

#### Fonts

| Section     | Font          |
| ----------- | ------------- |
| Navbar      | Macondo       |
| Headers     | Caveat        |
| Content     | Source Sans 3 |

The header/navigation font is Macondo - a stylised cal'igraphy font, used because it looks like an old bokshop sign. It is only used for larger text, so legibility isn't a concern.

Review headers are Caveat - mimics handwriting as you might find in a journal. This style might be harder to read in large blocks of text, but it is only used for shorter content such as book titles.

Review bodies are in Source Sans 3 - sans serif and uncomplicated. As the content of the reviews are longer sections of text, a more legible and easy to read font is used for accessibility.  
I considered using a monospaced or typewriter style font but, on testing, this was too distracting and difficult to read in large sections. 

#### Wireframes

### Responsivity

### User stories

My user stories focused on CRUD functionality, ease of use, account management, and accessibility. 

I used MoSCoW prioritisation and aimed for 60-70% must-have stories, in line with best practices.

I haven't detailed my won't-haves here, but some I considered are in the Future Features section above.

<details>
<summary>Complete User Stories</summary>

| User Story | Priorisation |
|------------|--------------|
| As a new user, I want to register an account so I can create and manage my own book reviews. | Must-have |
| As a user, I want to be able to log in to see my personal book reviews so I can see and add to my reading log. | Must-have |
| As a user, I want to have clear indication that I am logged in so I know I can access/edit my reviews. | Must-have |
| As a user, I want to see an error message and/or be redirected when I try to access a page without permission, so I understand what went wrong and how to fix it. | Must-have |
| As a user, I want to be able to see all of my book reviews so I can get an overview of my reading and/or find the review I want to read. | Must-have |
| As a user, I want to view a list of my book reviews with titles and ratings so I can quickly scan what I’ve read and how I felt about it. | Must-have |
| As a user, I want to be able to view a review in detail, so I can remember what I thought about a book and when I read it. | Must-have |
| As a user, I want to be able to add a new book review so I can record my thoughts and opinions on what I’ve read. | Must-have |
| As a user, I want to be able to edit a review I’ve submitted so I can update or change my thoughts over time. | Must-have |
| As a user, I want to be able to delete a review so I can remove mistakes or books I no longer want in my history. | Must-have |
| As a user, I want to see clear confirmation messages after adding, editing, or deleting a review so I know the action was successful. | Must-have |
| As a user with accessibility needs, I want to be able to access the site fully so I can record my reading. | Must-have |
| As a user, I want to be able to easily navigate the site so I can quickly get to the actions I want. | Must-have |
| As a mobile/desktop user, I want to be able to visit the site on all platforms so I can view and update my reading logs. | Must-have |
| As a user, I want to be able to rate my books easily, so I can quickly see what I thought without having to read the whole review. | Should-have |
| As a user, I want to see a confirmation message when I log in or log out, so I know the action was successful. | Should-have |
| As a new account holder, I want to see a clear message on my dashboard when it's empty so I know something hasn't gone wrong. | Should-have |
| As a visual user, I want to able to see book ratings in a star format, so I can easily see what rating was given. | Should-have |
| As a user, I want to be able to sort reviews by rating so I can see which books I most enjoyed, or that others enjoyed. | Should-have |
| As a user, I want to be able to sort reviews by author or book so I can find what I or other think of their work. | Should-have |
| As a user, I want to filter reviews (e.g. by author or rating) so I can find specific types of reviews. | Could-have |
| As busy user, I want to be able to save a review as a draft so I can come back and finish it later. | Could-have |
| As a visual user, I want to see the book covers associated with reviews so I can easily remember the book they're referencing. | Could-have |

</details>

### Agile

## Tech used 

## Testing

### Accessibility

#### Colour Contrast

All the colours used on the site were tested against WCAG colour contrast standards, to ensure each component stood out against the background for visually impaired users.

All compoments meet at least WCAG AA standards, with many meeting AAA.

The navigation section has a wood image as its background, with many colours within it. To test this I extracted the lightest colour found in the background and tested it against the font colour. It met WCAG for large text. All other colours in the image met WCAG AAA for both large and small text. Since the lightest colour in the image is not at all prevalent, I was happy with this result.

As a result of this test, I did have to darken the stars for the ratings slightly (to #9F7509), as the accent colour that's used elsewhere did not contrast well enough with the parchment of the review cards. With the darkened colour, the result was WCAG AA for icons.

<!-- Tab through site -->
<!-- naviagation consistent -->
<!-- labels on form fields -->
<!-- status updates screen reader - can screen readers read django messages -->
<!-- Semantic HTML/header order -->
<!-- Aria labels -->
### Lighthouse

### Manual Tests
<!-- test main features - your user stories , middle column is expected result, then actual result -->
<details>
<summary>Manual Test Log</summary>

| User Story | Expected Outcome | Actual Outcome |
|------------|------------------|----------------|
| As a new user, I want to register an account so I can create and manage my own book reviews. | | |
| As a user, I want to be able to log in to see my personal book reviews so I can see and add to my reading log. | | |
| As a user, I want to have clear indication that I am logged in so I know I can access/edit my reviews. | | |
| As a user, I want to see an error message and/or be redirected when I try to access a page without permission, so I understand what went wrong and how to fix it. | | |
| As a user, I want to be able to see all of my book reviews so I can get an overview of my reading and/or find the review I want to read. | | |
| As a user, I want to view a list of my book reviews with titles and ratings so I can quickly scan what I’ve read and how I felt about it. | | |
| As a user, I want to be able to view a review in detail, so I can remember what I thought about a book and when I read it. | | |
| As a user, I want to be able to add a new book review so I can record my thoughts and opinions on what I’ve read. | | |
| As a user, I want to be able to edit a review I’ve submitted so I can update or change my thoughts over time. | | |
| As a user, I want to be able to delete a review so I can remove mistakes or books I no longer want in my history. | ||
| As a user, I want to see clear confirmation messages after adding, editing, or deleting a review so I know the action was successful. || |
| As a user with accessibility needs, I want to be able to access the site fully so I can record my reading. | | |
| As a user, I want to be able to easily navigate the site so I can quickly get to the actions I want. | | |
| As a mobile/desktop user, I want to be able to visit the site on all platforms so I can view and update my reading logs. | | |
| As a user, I want to be able to rate my books easily, so I can quickly see what I thought without having to read the whole review. | | |
| As a user, I want to see a confirmation message when I log in or log out, so I know the action was successful. | | |
| As a new account holder, I want to see a clear message on my dashboard when it's empty so I know something hasn't gone wrong. | | |
| As a visual user, I want to able to see book ratings in a star format, so I can easily see what rating was given. | | |
| As a user, I want to be able to sort reviews by rating so I can see which books I most enjoyed, or that others enjoyed. | | |
| As a user, I want to be able to sort reviews by author or book so I can find what I or other think of their work. | | |
| As a user, I want to filter reviews (e.g. by author or rating) so I can find specific types of reviews. | | |
| As busy user, I want to be able to save a review as a draft so I can come back and finish it later. | | |
| As a visual user, I want to see the book covers associated with reviews so I can easily remember the book they're referencing. | | |

<!-- Also test on other browsers -->
</details>


### Unit Tests

### Validation

### Extant Bugs

## Deployment

## AI use
<!-- code creation -->
<!-- debugging -->
<!-- performance and UX improvements -->
<!-- Unit tests -->
<!-- AI influenced workflow, focusing on efficiency and outcomes without in-depth prompt documentation -->
## Credits
<!-- google fonts -->
