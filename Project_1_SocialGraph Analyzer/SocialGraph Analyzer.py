import json

# Load JSON from a file and return the parsed data structure.
def load_json(fname):
    with open(fname, "r") as f:
        data_blob = json.load(f)
    return data_blob


# Display all users and pages in a structured text format.
def show_users_and_pages(all_data):
    print("Users and Their Connections:\n")

    for usr in all_data.get("users", []):
        print(
            f"{usr.get('name')} (ID: {usr.get('id')}) "
            f"- Friends: {usr.get('friends')} "
            f"- Liked Pages: {usr.get('liked_pages')}"
        )

    print("\nPages:\n")
    for pg in all_data.get("pages", []):
        print(f"{pg['id']}: {pg['name']}")


# Clean the dataset by removing empty names, duplicates, and inactive users.
def clean_social_data(raw):
    # Filter out users with missing or blank names
    cleaned_users = []
    for one_user in raw["users"]:
        if one_user.get("name", "").strip():
            cleaned_users.append(one_user)
    raw["users"] = cleaned_users

    # Remove duplicate friend IDs for each user
    for u in raw["users"]:
        u_friends = set(u.get("friends", []))
        u["friends"] = list(u_friends)

    # Remove users who have no friends and no liked pages
    still_active = []
    for u in raw["users"]:
        if u.get("friends") or u.get("liked_pages"):
            still_active.append(u)
    raw["users"] = still_active

    # Remove duplicate page entries based on page ID
    uniq = {}
    for p in raw.get("pages", []):
        uniq[p["id"]] = p
    raw["pages"] = [val for val in uniq.values()]

    return raw


# Recommend pages for a given user based on similarity of liked pages with others.
def suggest_pages(uid, dataset):
    likes_map = {}
    for u in dataset["users"]:
        likes_map[u["id"]] = set(u.get("liked_pages", []))

    if uid not in likes_map:
        return []

    my_likes = likes_map[uid]
    scores = {}

    # Score pages by counting shared likes between users
    for other_id, liked_set in likes_map.items():
        if other_id == uid:
            continue

        shared = my_likes.intersection(liked_set)

        for pg in liked_set:
            if pg not in my_likes:
                scores[pg] = scores.get(pg, 0) + len(shared)

    sorted_res = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [x[0] for x in sorted_res]


# Recommend potential new friends based on the number of mutual friends.
def suggest_friends(uid, dataset):
    mapping = {}
    for u in dataset["users"]:
        mapping[u["id"]] = set(u.get("friends", []))

    if uid not in mapping:
        return []

    my_friends = mapping[uid]
    recs = {}

    # Count mutual friend connections for ranking
    for fr in my_friends:
        for pf in mapping.get(fr, []):
            if pf != uid and pf not in my_friends:
                recs[pf] = recs.get(pf, 0) + 1

    sorted_recs = sorted(recs.items(), key=lambda pair: pair[1], reverse=True)
    return [pair[0] for pair in sorted_recs]


# Main execution entrypoint: load, clean, display, and generate suggestions.
if __name__ == "__main__":
    messy_raw_data = load_json("codebook_data.json")
    tidied = clean_social_data(messy_raw_data)

    with open("cleaned_codebook_data.json", "w") as out:
        json.dump(tidied, out, indent=4)

    print("Data cleaned successfully!\n")

    show_users_and_pages(tidied)

    example_uid = 1
    print(f"\nPeople You May Know for User {example_uid}: {suggest_friends(example_uid, tidied)}")
    print(f"Pages You Might Like for User {example_uid}: {suggest_pages(example_uid, tidied)}")
