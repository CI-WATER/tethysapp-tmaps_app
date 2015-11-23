from tethys_apps.base import TethysAppBase, url_map_maker
from tethys_apps.base import PersistentStore
from tethys_apps.base import TethysAppBase, DatasetService
from tethys_apps.sdk import get_spatial_dataset_engine
from tethys_apps.sdk import list_spatial_dataset_engines

class FirstVersionTMAPS(TethysAppBase):
    """
    Tethys app class for First Version TMAPS.
    """

    name = 'TMAPS'
    index = 'tmaps_app:home'
    icon = 'tmaps_app/images/logo.jpg'
    package = 'tmaps_app'
    root_url = 'tmaps-app'
    color = '#347235'
        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='tmaps-app',
                           controller='tmaps_app.controllers.home'
                           ),
                    UrlMap(name='library',
                           url='tmaps-app/library',
                           controller='tmaps_app.controllers.library'
                           ),
                    UrlMap(name='makeyourown',
                           url='tmaps-app/make-your-own',
                           controller='tmaps_app.controllers.makeyourown'
                           ),
                    UrlMap(name='load',
                           url='tmaps-app/load',
                           controller='tmaps_app.controllers.load'
                           ),
                    UrlMap(name='preview',
                           url='tmaps-app/preview',
                           controller='tmaps_app.controllers.preview'
                           ),
        )

        return url_maps
        
        
    def dataset_services(self):
        """
        Add one or more dataset services
        """
        dataset_services = (DatasetService(name='tmaps_ckan',
                                           type='ckan',
                                           endpoint='http://ciwckan.chpc.utah.edu//api/3/action',
                                           apikey='4bd5fad7-e394-453e-9c05-dd34ed57c514'
                                           ),
        )

        return dataset_services
        
        
    def persistent_stores(self):
        """
        Add one or more persistent stores
        """
        stores = (PersistentStore(name='stream_gage_db',
                                  initializer='init_stores:init_stream_gage_db',
                                  spatial=True
                ),
        )

        return stores
        
