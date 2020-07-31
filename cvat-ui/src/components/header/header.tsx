// Copyright (C) 2020 Intel Corporation
//
// SPDX-License-Identifier: MIT

import './styles.scss';
import React from 'react';
import { RouteComponentProps } from 'react-router';
import { withRouter } from 'react-router-dom';
import { Row, Col } from 'antd/lib/grid';
import Layout from 'antd/lib/layout';
import Icon from 'antd/lib/icon';
import Button from 'antd/lib/button';
import Menu from 'antd/lib/menu';
import Dropdown from 'antd/lib/dropdown';
import Modal from 'antd/lib/modal';
import Text from 'antd/lib/typography/Text';

import { CVATLogo, AccountIcon } from 'icons';
import consts from 'consts';

interface HeaderContainerProps {
    onLogout: () => void;
    logoutFetching: boolean;
    installedAnalytics: boolean;
    installedAutoAnnotation: boolean;
    installedTFAnnotation: boolean;
    installedTFSegmentation: boolean;
    serverHost: string;
    username: string;
    toolName: string;
    serverVersion: string;
    serverDescription: string;
    coreVersion: string;
    canvasVersion: string;
    uiVersion: string;
    switchSettingsShortcut: string;
}

type Props = HeaderContainerProps & RouteComponentProps;

function HeaderContainer(props: Props): JSX.Element {
    const {
        installedTFSegmentation,
        installedAutoAnnotation,
        installedTFAnnotation,
        installedAnalytics,
        username,
        toolName,
        serverHost,
        serverVersion,
        serverDescription,
        coreVersion,
        canvasVersion,
        uiVersion,
        onLogout,
        logoutFetching,
        switchSettingsShortcut,
    } = props;

    const renderModels = installedAutoAnnotation
        || installedTFAnnotation
        || installedTFSegmentation;

    const {
        CHANGELOG_URL,
        LICENSE_URL,
        GITTER_URL,
        FORUM_URL,
        GITHUB_URL,
    } = consts;

    function aboutModal(): void {
        Modal.info({
            title: `${toolName}`,
            content: (
                <div>
                    <p>
                        {`${serverDescription}`}
                    </p>
                    <p>
                        <Text strong>
                            Server version:
                        </Text>
                        <Text type='secondary'>
                            {` ${serverVersion}`}
                        </Text>
                    </p>
                    <p>
                        <Text strong>
                            Core version:
                        </Text>
                        <Text type='secondary'>
                            {` ${coreVersion}`}
                        </Text>
                    </p>
                    <p>
                        <Text strong>
                            Canvas version:
                        </Text>
                        <Text type='secondary'>
                            {` ${canvasVersion}`}
                        </Text>
                    </p>
                    <p>
                        <Text strong>
                            UI version:
                        </Text>
                        <Text type='secondary'>
                            {` ${uiVersion}`}
                        </Text>
                    </p>
                    <Row type='flex' justify='space-around'>
                        <Col><a href={CHANGELOG_URL} target='_blank' rel='noopener noreferrer'>{'What\'s new?'}</a></Col>
                        <Col><a href={LICENSE_URL} target='_blank' rel='noopener noreferrer'>License</a></Col>
                        <Col><a href={GITTER_URL} target='_blank' rel='noopener noreferrer'>Need help?</a></Col>
                        <Col><a href={FORUM_URL} target='_blank' rel='noopener noreferrer'>Forum on Intel Developer Zone</a></Col>
                    </Row>
                </div>
            ),
            width: 800,
            okButtonProps: {
                style: {
                    width: '100px',
                },
            },
        });
    }

    const menu = (
        <Menu className='cvat-header-menu' mode='vertical'>
            <Menu.Item
                title={`Press ${switchSettingsShortcut} to switch`}
                onClick={
                    (): void => props.history.push('/settings')
                }
            >
                <Icon type='setting' />
                Settings
            </Menu.Item>
            <Menu.Item onClick={() => aboutModal()}>
                <Icon type='info-circle' />
                About
            </Menu.Item>
            <Menu.Item
                onClick={onLogout}
                disabled={logoutFetching}
            >
                {logoutFetching ? <Icon type='loading' /> : <Icon type='logout' />}
                Logout
            </Menu.Item>

        </Menu>
    );

    return (
        <Layout.Header className='cvat-header'>
            <div className='cvat-left-header'>
                <Icon className='cvat-logo-icon' component={CVATLogo} />

                <Button
                    className='cvat-header-button'
                    type='link'
                    value='tasks'
                    onClick={
                        (): void => props.history.push('/tasks?page=1')
                    }
                >
                    Tasks
                </Button>
                { renderModels
                    && (
                        <Button
                            className='cvat-header-button'
                            type='link'
                            value='models'
                            onClick={
                                (): void => props.history.push('/models')
                            }
                        >
                            Models
                        </Button>
                    )}
                { installedAnalytics
                    && (
                        <Button
                            className='cvat-header-button'
                            type='link'
                            onClick={
                                (): void => {
                                    // false positive
                                    // eslint-disable-next-line
                                    window.open(`${serverHost}/analytics/app/kibana`, '_blank');
                                }
                            }
                        >
                            Analytics
                        </Button>
                    )}
            </div>
            <div className='cvat-right-header'>
                <Button
                    className='cvat-header-button'
                    type='link'
                    onClick={
                        (): void => {
                            // false positive
                            // eslint-disable-next-line security/detect-non-literal-fs-filename
                            window.open(GITHUB_URL, '_blank');
                        }
                    }
                >
                    <Icon type='github' />
                    <Text className='cvat-text-color'>GitHub</Text>
                </Button>
                <Button
                    className='cvat-header-button'
                    type='link'
                    onClick={
                        (): void => {
                            // false positive
                            // eslint-disable-next-line
                            window.open(`${serverHost}/documentation/user_guide.html`, '_blank')
                        }
                    }
                >
                    <Icon type='question-circle' />
                    Help
                </Button>
                <Dropdown overlay={menu} className='cvat-header-menu-dropdown'>
                    <span>
                        <Icon className='cvat-header-account-icon' component={AccountIcon} />
                        <Text strong>
                            {username.length > 14 ? `${username.slice(0, 10)} ...` : username}
                        </Text>
                        <Icon className='cvat-header-menu-icon' type='caret-down' />
                    </span>
                </Dropdown>
            </div>
        </Layout.Header>
    );
}

export default withRouter(HeaderContainer);
