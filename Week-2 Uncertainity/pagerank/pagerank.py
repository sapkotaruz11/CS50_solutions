import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    random_prob = 1 - damping_factor
    N = len(corpus)
    transitional_probabilities = {}

    if (corpus[page] == None):
        for pages in corpus:
            transitional_probabilities[pages] = 1 / N

    else:

        for links in corpus:
            transitional_probabilities[links] = random_prob / N
            if links in corpus[page]:
                transitional_probabilities[links] += damping_factor / len(corpus[page])

    return transitional_probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}
    sample_page = None
    random.seed()

    for page in corpus:
        page_rank[page] = 0

    for sample in range(n):
        if sample_page is None:

            sample_page = random.choices(list(corpus.keys()), k=1)[0]
        else:

            model = transition_model(corpus, sample_page, damping_factor)
            sample_page = random.choices(list(model.keys()), weights=list(model.values()), k=1)[0]

        page_rank[sample_page] += 1

    for page in corpus:
        page_rank[page] /= n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}
    num_links = {}
    page_rank_threshold = 0.001
    N = len(corpus)
    for page in corpus:
        page_rank[page] = 1 / N
        if len(corpus[page]) > 0:
            num_links[page] = len(corpus[page])
        else:
            num_links[page] = N
    while True:

        page_rank_old = copy.deepcopy(page_rank)
        for page in page_rank:
            summ = float(0)
            for check_page in corpus:
                if page in corpus[check_page] or corpus[check_page] == set():
                    summ += page_rank_old[check_page] / num_links[check_page]
            page_rank[page] = damping_factor * summ + ((1 - damping_factor) / N)
        break_while = False

        for page in page_rank:
            diff = abs(page_rank[page] - page_rank_old[page])
            if diff < page_rank_threshold:
                break_while = True
            else:
                break_while = False
        if break_while:
            break
    return page_rank


if __name__ == "__main__":
    main()
