import React, { useEffect,useContext } from 'react'
import { Store } from '../../store/index'
import { fetchRelatedData } from '../../apis/index'
import SideListItem from '../SideListItem/SideListItem'
import Style from './SideList.module.scss'

const SideList = () => {
    const { globalState, setGlobalState } =useContext(Store)
    const setRelatedVideo = async (id) => {
        await fetchRelatedData(id).then((res) => {
            setGlobalState({type: 'SET_RELATED', payload: {related: res.data.items}})
        })
    }
    useEffect(() => {
        setRelatedVideo(globalState.selected.id)
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [globalState.selected])
    return (
        <div className={Style.sidenav}>
            {
                globalState.related ? globalState.related.map((related) => {
                    return (
                        <SideListItem
                            id={related.id.videoId}
                            key={related.id.videoId}
                            src={related.snippet.thumbnails.medium.url}
                            title={related.snippet.title}
                        />
                    )
                }) : <span>no data</span>
            }
        </div>
    )
}

export default SideList
