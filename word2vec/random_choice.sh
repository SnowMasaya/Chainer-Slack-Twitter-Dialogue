jot -r "$(wc -l jawiki-latest-all-titles-in-ns0)" 1 | paste - jawiki-latest-all-titles-in-ns0 | sort -n | cut -f 2- | head -n 5000
