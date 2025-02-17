from supabase import create_client, Client
import os
from pushover import Pushover

def main():
    supabase: Client = create_client("https://urpytqjjpixevrhbzkvx.supabase.co", os.environ['SUPABASE_API_KEY'])
    po = Pushover(os.environ['PUSHOVER_APP_TOKEN'])
    po.user(os.environ['PUSHOVER_USER_TOKEN'])
    response = supabase.rpc("get_random_fact", params={}).execute()
    if not response.data:
        empty_msg = po.msg("We have run out of facts! Resetting db and will return tomorrow.")
        empty_msg.set("title", "uh oh")
        po.send(empty_msg)
        exit(0)
    fact = response.data[0]
    fact_id = fact.get('id')
    fact_text = fact.get('fact_text')
    msg = po.msg(fact_text)
    msg.set("title", "Football Fact of the Day")
    po.send(msg)
    supabase.table("football_facts").update({"sent_status": "true"}).eq("id", fact_id).execute()

# Call the main function if this script is run directly
if __name__ == "__main__":
    main()

