from utils.helper_utils import remove_expired_sessions

async def clean_up_session():
    print("Starting scheduler. Running session clean up in the background.")
    process_done = await remove_expired_sessions()
    print(process_done)
