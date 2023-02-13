from server.resources.run_biogpt import RunBioGptApi


def init_routes(api):
    api.add_resource(RunBioGptApi, '/api/run_biogpt')
