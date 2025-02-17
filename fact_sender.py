from supabase import create_client, Client
import Constants
from pushover import Pushover

def main():
    supabase: Client = create_client("https://urpytqjjpixevrhbzkvx.supabase.co", Constants.SUPABASE_API_KEY)
    response = supabase.rpc("get_random_fact", params={}).execute()
    fact = response.data[0]
    fact_id = fact.get('id')
    fact_text = fact.get('fact_text')
    po = Pushover(Constants.PUSHOVER_APP_TOKEN)
    po.user(Constants.PUSHOVER_USER_TOKEN)

    msg = po.msg(fact_text)
    msg.set("title", "Football Fact of the Day")
    po.send(msg)

    # supabase.table("football_facts").update({"sent_status": "true"}) .eq("id", fact_id).execute()




# Call the main function if this script is run directly
if __name__ == "__main__":
    main()

