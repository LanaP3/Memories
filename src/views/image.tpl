% rebase('base.tpl', current_page = "image", note=None, error=None)

<div class = "card">
    <div class="card-image">
        <figure class="image">
            <img src="{{ get_url('database', filename= image.id) }}" >
        </figure>
    </div>
    <footer class="card-footer">
        <p class="card-footer-item">
            <form action="/like/" method="POST">
                    {{len(image.likes)}}
                <button class="icon">
                    <i class="fa-regular fa-heart"></i>   
                </button>
            </form>
        </p>
        <p class="card-footer-item">
            <form action="/dislike/" method="POST">
                    {{len(image.dislikes)}}
                <button class="icon">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </form>
        </p>
    </footer>
</div>

<article class = "media">
    <div class = "media-content">
       <div class = "content">
            %for comment in image.comments:                    
            <strong>{{comment[0]}}</strong>
            <br>
            <p>
            {{comment[1]}}
            </p>
            %end
        </div>
        <form action="/add_comment/" method="POST">
            <div class="field">
                <div class="control has-icons-left">
                    <input class="input" name="comment" type="text" placeholder="Add a comment...">
                    <span class="icon is-small is-left">
                        <i class="fa fa-pencil"></i>
                    </span>
                </div>
            </div>
            <div class="field is-grouped">
                <div class="control">
                    <button class="button is-link">Submit</button>
                </div>
            </div>
        </form>
    </div>
</article>

  