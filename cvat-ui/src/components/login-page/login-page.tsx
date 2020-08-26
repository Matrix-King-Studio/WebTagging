// Copyright (C) 2020 Intel Corporation
//
// SPDX-License-Identifier: MIT

import React from 'react';
import { RouteComponentProps } from 'react-router';
import { Link, withRouter } from 'react-router-dom';
import Title from 'antd/lib/typography/Title';
import Text from 'antd/lib/typography/Text';
import { Row, Col } from 'antd/lib/grid';

import LoginForm, { LoginData } from './login-form';
import CookieDrawer from './cookie-policy-drawer';

interface LoginPageComponentProps {
    fetching: boolean;
    onLogin: (username: string, password: string) => void;
}

function LoginPageComponent(props: LoginPageComponentProps & RouteComponentProps): JSX.Element {
    const sizes = {
        xs: { span: 14 },
        sm: { span: 14 },
        md: { span: 10 },
        lg: { span: 4 },
        xl: { span: 4 },
    };

    const {
        fetching,
        onLogin,
    } = props;

    return (
        <>
            <Row type='flex' justify='center' align='middle'>
                <Col {...sizes}>
                    <Title level={2}> 登录 </Title>
                    <LoginForm
                        fetching={fetching}
                        onSubmit={(loginData: LoginData): void => {
                            onLogin(loginData.username, loginData.password);
                        }}
                    />
                    <Row type='flex' justify='start' align='top'>
                        <Col>
                            <Text strong>
                                <Link to='/auth/register'>注册</Link>
                            </Text>
                        </Col>
                    </Row>
                </Col>
            </Row>
            <CookieDrawer />
        </>
    );
}

export default withRouter(LoginPageComponent);
