% rebase('base.tpl')
<p>{{username}}</p>
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
  <input class="form-control" type="submit" value="Start upload" />
</form>
<br>

%for album in albums:
<form>
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">{{album_name}}</button>
        </div>
    </div>
</form>
%end

<p>
%for image in images:
{{image_id}}
%end
</p>
