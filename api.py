import aiohttp
"""
Concurrent API Calls done using asynchronous functions and the aiohttp library

Cache is held within the ApiConnection instance
- Whenever an api call is made with a tag, we add that tag and the results to the cache as a key and value pair
- Subsequent API calls will check the cache before making an API request
- We could add a timeout on the cache so it does not hold data until the application restarts

"""

class ApiConnection:
    def __init__(self):
        self.url = "https://api.REDACTED.io/assessment/blog/posts" 
        self.cache = dict() # the cache will persist as long as the instance of the class does

    async def gather(self, tags): # concurrent approach to making requests
        """
        This function takes a list of tags and makes concurrent requests to the API for each tag
        The function also checks the cache before making a call, if the tag is already in the 
        cache we can retreive the data directly from there instead

        The function makes sure only unique blogs are added by keeping a set of all added blogs
        If a blog had been added under a different tag, it is not added again
        Blogs are identified by their unique id

        This function returns a list of all unique blogs  
        """
        async with aiohttp.ClientSession() as sess:
            results = {"posts": []}
            posts = results["posts"]
            ids = set()
            for tag in tags:

                # checks if the tag we need is already in the cache, if so, we simply retrieve the value
                if tag in self.cache:
                    print("Request in cache already:", tag)
                    cur_posts = self.cache[tag]
                else:
                    async with sess.get(url=self.url, params={'tag': tag}) as res:
                        cur_posts = await res.json()
                        print("Added tag to cache:", tag)
                        self.cache[tag] = cur_posts
                for blog in cur_posts['posts']:
                    id = blog.get('id')
                    if id not in ids:
                        posts.append(blog)
                        ids.add(id) 
            return results
                
    async def get_related_blogs(self, tag, sess):
        """
        Takes a specific id and makes the request to the API under the current Client Session

        Returns the response as JSON
        """
        res = await sess.get(url=self.url, params={'tag': tag})
        return res.json()