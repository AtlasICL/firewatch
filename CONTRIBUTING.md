### Code style
- For Python style guide, please see the official [PEP 8 Style Guide](https://peps.python.org/pep-0008/).
- Always document your functions using the correct documentation format.
- Prefer long, descriptive function and variable names over explanatory comments.
- Comments should never _reiterate_ what the code does in English. Comments
  should only exist to explain _why_ we have some code, or _why_ we make some
  decision instead of another method.
- Use interfaces and robust types. Never hesitate to create a custom struct or
  enum to better represent some input or output datatype.

### Testing
- We use [unittest](https://docs.python.org/3/library/unittest.html).
- Install the development dependencies (test, benchmark and lint tooling)
  with `pip install -r requirements-dev.txt`.
- Run everything with `just test`, or a subset with TODO.
- Performance benchmarks live in `benchmarks/` and are left out of
  `just test` to keep it fast. Run them on demand with `just perf`.

### Repo hygiene
- Always rebase, and never merge main into your feature branch. See
  [video](https://www.youtube.com/watch?v=DkWDHzmMvyg).
- Each commit should represent one unit of work. You should commit coherent
  logical changes. There should be no work in progress commits pushed up (it's
  fine temporarily locally). If you need to save your work and pick up later,
  you may commit, and then amend the commit later.
- Rebase over merge. You should set your gitconfig to make sure you always
  `git pull --rebase`, and not raw `git pull`.
- Similarly, if you've been working on some changes locally, and others have
  made changes to remote main in the meantime, you should follow
  [this procedure](#rebase-procedure).
- If you've committed something, and then realise you need to change something
  small, do a `commit --amend --no-edit`. 
- When necessary, use `push --force-with-lease` and not `push --force`.
- Commit messages should always follow the [Conventional Commits standard](https://www.conventionalcommits.org/en/v1.0.0/#specification),
  for instance `"fix(gui): make new file button colour blue for consistency"`.
- Use GitHub Issues, and link them in your PR when appropriate. 

#### Rebase procedure
```
git stash
git switch main
git fetch origin
git pull --rebase
git switch <your_branch>
git rebase main
```

If at this point, git has rebased successfully, then you can `git stash pop`.
If, on the other hand, there are merge conflicts, then resolve them in VS Code,
and once finished resolving, run `git rebase --continue` (after which you can
do `git stash pop`).