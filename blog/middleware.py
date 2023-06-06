import pynecone as pc


class CloseSidebarMiddleware(pc.Middleware):
    def preprocess(self, app, state, event):
        if event.name == pc.event.get_hydrate_event(state):
            state.get_substate(["navbar_state"]).sidebar_open = False
