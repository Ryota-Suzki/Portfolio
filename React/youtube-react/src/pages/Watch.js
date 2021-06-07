import React from 'react'
import Layout from '../components/Layout/Layout'
import SideList from '../components/SideList/SideList'
import VideoDetail from '../components/VideoDetail/VideoDetail'

const Watch = () => {
    return (
        <Layout>
            <VideoDetail />
            <SideList />
        </Layout>
    )
}

export default Watch
