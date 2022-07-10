% rebase('base.tpl')
<p>{{username}}</p>
<form action="/log_out/" method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">Log out</button>
        </div>
    </div>
</form>

<form method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">new album</button>
        </div>
    </div>
</form>
<br>
<form action="/main_page/" enctype="multipart/form-data">
  Upload new photo: <input type="file" name="upload" />
  <input class="form-control" type="submit" value="upload" />
</form>
<br>

%for album in albums:
<form action="/album/" method="get">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">album</button>
        </div>
    </div>
</form>
%end


%for image in images:
<p>{{image}}</p>

<form action="/add_to_album/" method="POST">
    <div class="field">
        <div class="control has-icons-left">
            <input class="input" name="album" type="text" placeholder="album">
            <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
            </span>
        </div>
    </div>
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">add to album</button>
        </div>
    </div>
%if album:
<p class="help is-danger">{{image}} has been added to **ALBUM**.</p>
%end
</form>
%end

