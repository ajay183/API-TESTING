import requests
import time
import threading

# Define function to make API request and return time to first byte and total load time
def test_api_performance(url):

# Make API request
start_time = time.time()
response = requests.get(url)
ttfb = time.time() - start_time

# Get total load time by checking content-length header
content_length = response.headers.get('content-length')
if content_length:
total_load_time = int(content_length) / (1024 * 1024) / ttfb
else:
total_load_time = None

return ttfb, total_load_time

# Define function to test API performance during parallel requests
def test_parallel_performance(url, num_requests):

# Create list to store thread objects
threads = []

# Create thread for each API request and add to list
for i in range(num_requests):
thread = threading.Thread(target=test_api_performance, args=(url,))
thread.start()
threads.append(thread)

# Wait for all threads to finish
for thread in threads:
thread.join()

# Calculate average time to first byte and total load time
avg_ttfb = sum([thread.ttfb for thread in threads]) / num_requests
avg_total_load_time = sum([thread.total_load_time for thread in threads]) / num_requests

return avg_ttfb, avg_total_load_time

# Define API endpoint URL
url = "https://api.example.com/endpoint"

# Test API performance and print results
ttfb, total_load_time = test_api_performance(url)
print("Time to first byte:", ttfb)
print("Total load time:", total_load_time)

# Test parallel performance and print results
num_requests = 10
avg_ttfb, avg_total_load_time = test_parallel_performance(url, num_requests)
print("Average time to first byte during parallel requests:", avg_ttfb)
print("Average total load time during parallel requests:", avg_total_load_time)