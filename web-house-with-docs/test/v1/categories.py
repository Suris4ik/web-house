from requests import get, post, put, delete

print('get categories')
print(get('http://localhost:8080/api/v1/categories').json())
print('add category')
print(post('http://localhost:8080/api/v1/categories',
           json={'name': 'cat1'}).json())
print('get 1 category')
print(get('http://localhost:8080/api/v1/categories/4').json())
print('update category')
print(put('http://localhost:8080/api/v1/categories/4',
          json={'name': 'cat2'}).json())
print('updated category')
print(get('http://localhost:8080/api/v1/categories/4').json())
print('delete category')
print(delete('http://localhost:8080/api/v1/categories/4').json())
print('all categories')
print(get('http://localhost:8080/api/v1/categories').json())
