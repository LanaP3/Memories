% rebase('base.tpl', current_page=album.name, error=error)


<form action="/remove_album/" method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link has-background-grey-light	">
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

<div class="tile is-ancestor">
    <article class="tile is-child box">
        <div>
        <b>ALBUM NAME:</b>  {{album.name}}<br/>
        <b>ADMIN:</b>  {{album.owner}}<br/>
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
                    <button class="button is-link has-background-grey-light">
                    add friend
                    </button>
                </div>
            </div>
        </form>
        % end
    </article>
</div>

<div class="tile">
    <article class="tile is-parent">
        % for image_id in list(album.images):
        <div class="tile">
            <article class="tile is-child box">
                <img src= "{{ get_url('database', filename= image_id) }}" class="img-fluid" />
                <form action="/image/{{image_id}}" method="POST">
                    <div class="field is-grouped">
                        <div class="control">
                            <button class="button is-link">
                            <i class="fa fa-bars" aria-hidden="true"></i>
                            </button>
                        </div>
                    </div>
                </form>
            </article>
        </div>
        % end
    </article>
</div>