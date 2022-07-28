#!/bin/bash

numCommitsToAnalyze=1000

# code matches are case sensitive
# we're excluding package.json and package-lock.json
# also excluding "console.log" otherwise there is way too much noise
codeDiffFlagsRegex="\.HTML|\.txt|\.json|\.sql|\.sqlite|\.xml|\.xhtml|\.csv|\.css|\.tsv|\.yaml|\.log|\.cnf|\.conf|\.cfg|.zip"
codeDiffNotEqualRegex="console.log|package.json|package-lock.json"
commits=(`git rev-list --branches $branch`)
declare -a rel_commits
commit_ind=1
while (( $commit_ind < ${#commits[@]} && ${#rel_commits[@]} < $numCommitsToAnalyze )); do
	cur_commit=${commits[$commit_ind]}
	mod_files=`git diff-tree --no-commit-id --name-only -r $cur_commit`
	getNumRelFilesPy=`cat <<EOF
dev_test_paths = [ "test", "package.json" ] # paths to ignore: tests, and package.json 
rel_extensions = [ "js", "ts", "cjs", "mjs" ]
sub_rel_extensions = [ "HTML", "txt", "json", "sql", "sqlite", "xml", "xhtml", "csv", "css", "tsv", "yaml", "log", "cnf", "conf", "cfg", ".zip"]
rel_files = [ f for f in """$mod_files""".split("\n") if rel_extensions.count( f.split(".")[-1]) > 0 and sum([ f.count(d) for d in dev_test_paths]) == 0]
sub_rel_files = [ f for f in """$mod_files""".split("\n") if sub_rel_extensions.count( f.split(".")[-1]) > 0 and sum([ f.count(d) for d in dev_test_paths]) == 0]
types_of_rel_files = 0
if len(rel_files) > 0:
	types_of_rel_files = 2 if len(sub_rel_files) > 0 else 1
print( types_of_rel_files)
EOF`
	numRelFiles=`python -c "$getNumRelFilesPy"`
	diffWithParentCodeUpdateCount=`git diff ${cur_commit}^! | grep -Ec "${codeDiffFlagsRegex}"`
	diffWithParentCodeUpdateCountExcluded=`git diff ${cur_commit}^! | grep -Ec "${codeDiffNotEqualRegex}"`
	if ((( $diffWithParentCodeUpdateCount != $diffWithParentCodeUpdateCountExcluded || $numRelFiles > 1 ) && $numRelFiles > 0 )); then
		rel_commits=(${rel_commits[@]} $cur_commit)
	fi
	(( commit_ind = $commit_ind + 1 ))
done

# function to get an array as csv
join () {
  local IFS="$1"
  shift
  echo "$*"
}

join , "${rel_commits[@]}" 
