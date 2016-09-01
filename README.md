# tripawiser
A wise trip planner for San Francisco at www.tripawiser.xyz

Presentation available at https://docs.google.com/presentation/d/13Z9xFqrxtlnzbhiaInLPnXtHKi5vJhmraMufm21uYIk/present?slide=id.p

Breif Description of Code (in order of execution):

1. data_extraction_attractions_list: collects names of all attractions from TripAdvisor

2. data extraction_attractions_info: collects info on all attractions like address, recommeneded length of visits, urls, categories, reviews and ratings

3. data extraction_attractions_reviews: scrapes reviews of all attractions

4. topic_modeling: uses LDA to do topic modeling on attraction reviews

5. topic_modeling_labeling_editing: cleaning and labeling the topics from topic_modeling

6. optimal_tour: given a list of attractions, their prizes and specified time, finds the tour with maximum prize which can be finished in specified time using dynamic programming implementation of a prize collecting version of traveling salesman problem

7. main_fun: takes in user interests, specified time and starting addresses and outputs a specialized itinerary for a tourist

8. app/optimal_tour_app: app version of the optimal_tour file

9. app/main_fun_app: app version of the main_fun file

10. app/views: interface through which flask interacts with the browser
