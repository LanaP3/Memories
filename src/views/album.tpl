% rebase('base.tpl', current_page = album.name)


<form action="/remove_album/" method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">
            <i class="fa-solid fa-trash"></i>
            % if account.username==album.owner:
            <sub>DELETE ALBUM</sub>
            % else:
            <sub>LEAVE ALBUM</sub>
            % end
            </button>
        </div>
    </div>
</form>


<div>
<b>ALBUM NAME:</b>  {{album.name}}<br/>
<b>CREATOR:</b>  {{album.owner}}<br/>
<b>DATE:</b>  {{album.date_added}}<br/>
<b>PEOPLE:</b>  {{str_of_people}}
</div>

% if account.username==album.owner:
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
% if error:
<p class="help is-danger">{{error}}</p>
% end
</form>
% end

% for image_id in list(album.images):
<div>
<img src= "{{ get_url('database', filename= image_id) }}" class="img-fluid" />
</div>
<form action="/image/{{image_id}}" method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">
            <i class="fa fa-bars" aria-hidden="true"></i>
            </button>
        </div>
    </div>
</form>
% end