from requests import get, post, put, delete

print('get posts')
print(get('http://localhost:8080/api/v2/posts').json())
print('add post')
print(post('http://localhost:8080/api/v2/posts',
           json={'film_id': 1, 'user_id': 1, 'body': 'great film', 'categories': [1, 2]}).json())
print('get 1 post')
print(get('http://localhost:8080/api/v2/posts/5').json())
print('update post')
print(put('http://localhost:8080/api/v2/posts/5',
          json={'film_id': 1, 'user_id': 1,'categories': [1, 2], 'body': 'awful film'}).json())
print('updated post')
print(get('http://localhost:8080/api/v2/posts/5').json())
print('delete post')
print(delete('http://localhost:8080/api/v2/posts/5').json())
print('all posts')
print(get('http://localhost:8080/api/v2/posts').json())
