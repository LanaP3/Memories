% rebase('base.tpl', current_page=album.name)

<p>
{{album.name}}
</p>

%if account.username==album.owner:
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
%if error:
<p class="help is-danger">{{error}}</p>
%end
</form>
%end

%for image in album.images:
<form action="/image/" method="get">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">image</button>
        </div>
    </div>
</form>