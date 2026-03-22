from nicegui import ui, app
from api_client import client

def run_gui():
    @ui.page('/login')
    def login_page():
        with ui.card().classes('absolute-center w-96'):
            ui.label('Social Media App - Login').classes('text-2xl font-bold mb-4')
            username = ui.input('Username').classes('w-full mb-2')
            password = ui.input('Password', password=True, password_toggle_button=True).classes('w-full mb-4')
            
            def do_login():
                res, status = client.login(username.value, password.value)
                if status == 200:
                    ui.notify('Login successful!', type='positive')
                    ui.navigate.to('/')
                else:
                    ui.notify(f'Login failed: {res.get("detail", "Error")}', type='negative')

            ui.button('Login', on_click=do_login).classes('w-full mb-2')
            ui.button('Register Instead', on_click=lambda: ui.navigate.to('/register'), color='secondary').classes('w-full')

    @ui.page('/register')
    def register_page():
        with ui.card().classes('absolute-center w-96'):
            ui.label('Register Account').classes('text-2xl font-bold mb-4')
            username = ui.input('Username').classes('w-full mb-2')
            email = ui.input('Email').classes('w-full mb-2')
            password = ui.input('Password', password=True).classes('w-full mb-4')
            
            def do_register():
                res, status = client.register(username.value, email.value, password.value)
                if status == 201:
                    ui.notify('Registration successful! Please login.', type='positive')
                    ui.navigate.to('/login')
                else:
                    ui.notify(f'Registration failed: {res.get("detail", "Error")}', type='negative')

            ui.button('Register', on_click=do_register).classes('w-full mb-2')
            ui.button('Back to Login', on_click=lambda: ui.navigate.to('/login'), color='secondary').classes('w-full')

    @ui.page('/')
    def home_page():
        if not client.token:
            ui.navigate.to('/login')
            return

        with ui.header(elevated=True).classes('flex items-center justify-between'):
            ui.label('Social Feed').classes('text-xl font-bold')
            with ui.row().classes('items-center'):
                ui.label(client.username).classes('font-bold mr-4')
                ui.button('New Post', on_click=lambda: ui.navigate.to('/create'))
                ui.button('Logout', color='red', on_click=lambda: (client.logout(), ui.navigate.to('/login')))

        search_input = ui.input('Search Posts...', on_change=lambda e: load_posts(e.value)).classes('w-full max-w-2xl mx-auto mt-4')

        posts_container = ui.column().classes('w-full max-w-2xl mx-auto mt-4')

        def load_posts(search=""):
            posts_container.clear()
            posts = client.get_posts(search)
            with posts_container:
                for post in posts:
                    with ui.card().classes('w-full mb-4'):
                        with ui.row().classes('justify-between items-center w-full'):
                            ui.label(post['title']).classes('text-lg font-bold')
                            # Delete option
                            def delete_p(p_id=post['id']):
                                status = client.delete_post(p_id)
                                if status == 204:
                                    ui.notify('Deleted successfully', type='positive')
                                    load_posts(search_input.value)
                                else:
                                    ui.notify('Cannot delete this post (only owner can delete)', type='negative')

                            ui.button(icon='delete', color='red', on_click=delete_p).props('flat round size=sm')

                        ui.label(post['content']).classes('mb-2 text-gray-700 whitespace-pre-wrap')
                        with ui.row().classes('items-center justify-between w-full mt-2'):
                            ui.label(f"By {post['owner']['username']}").classes('text-sm text-gray-500')
                            
                            def vote(p_id=post['id']):
                                res, status = client.vote(p_id, 1)
                                if status == 201:
                                    ui.notify('Voted!', type='positive')
                                    load_posts(search_input.value)
                                else:
                                    ui.notify(str(res.get('detail', 'Could not vote')), type='warning')
                            
                            ui.button(f"Upvote ({post['votes']})", on_click=vote).props('outline rounded size=sm')

        # Initial load
        load_posts()

    @ui.page('/create')
    def create_page():
        if not client.token:
            ui.navigate.to('/login')
            return

        with ui.header(elevated=True).classes('flex items-center justify-between'):
            ui.label('Create Post').classes('text-xl font-bold')
            with ui.row().classes('items-center'):
                ui.label(client.username).classes('font-bold mr-4')
                ui.button('Back', on_click=lambda: ui.navigate.to('/'), color='secondary')

        with ui.card().classes('w-full max-w-2xl mx-auto mt-8'):
            title = ui.input('Title').classes('w-full mb-4')
            content = ui.textarea('Content').classes('w-full mb-4')
            
            def submit():
                res, status = client.create_post(title.value, content.value)
                if status == 201:
                    ui.notify('Post created!', type='positive')
                    ui.navigate.to('/')
                else:
                    ui.notify(f'Failed: {res.get("detail", "Error")}', type='negative')

            ui.button('Submit', on_click=submit).classes('w-full')

    ui.run(port=8080, title="Social Media App")

if __name__ in {"__main__", "__mp_main__"}:
    run_gui()
