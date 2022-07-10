% rebase('base.tpl')
<p>{{username}}</p>
<form action="/" method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">Log out</button>
        </div>
    </div>
</form>

<form action="/main_page/" method="get">
    <input name = main_page value="main page" type="submit" class="btn btn-outline-primary"/>
</form>
<p>
{{album}}
</p>
<form action="/add_friend/" method="POST">
    <div class="field">
        <div class="control has-icons-left">
            <input class="input" name="friend" type="text" placeholder="friend's name">
            <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
            </span>
        </div>
    </div>
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">add friend</button>
        </div>
    </div>
%if friend:
<p class="help is-danger">{{friend}} has been added to the album.</p>
%end
</form>

<form method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">add photo</button>
        </div>
    </div>
</form>

%for image in images:
{{image}}
<form action="/gallery" method="post">
    <option value="likes">Likes</option>
</form>
%end
</p>