// Copyright (C) 2020 Intel Corporation
//
// SPDX-License-Identifier: MIT

import React from 'react';
import { Row, Col } from 'antd/lib/grid';
import Pagination from 'antd/lib/pagination';

import ModelRunnerModalContainer from 'containers/model-runner-dialog/model-runner-dialog';
import TaskItem from 'containers/tasks-page/task-item';

export interface ContentListProps {
    onSwitchPage(page: number): void;
    currentTasksIndexes: number[];
    currentPage: number;
    numberOfTasks: number;
}

export default function TaskListComponent(props: ContentListProps): JSX.Element {
    const {
        currentTasksIndexes,
        numberOfTasks,
        currentPage,
        onSwitchPage,
    } = props;
    const taskViews = currentTasksIndexes.map(
        (tid, id): JSX.Element => <TaskItem idx={id} taskID={tid} key={tid} />,
    );

    return (
        <>
            <Row type='flex' justify='center' align='middle'>
                <Col className='cvat-tasks-list' md={22} lg={18} xl={16} xxl={14}>
                    { taskViews }
                </Col>
            </Row>
            <Row type='flex' justify='center' align='middle'>
                <Col md={22} lg={18} xl={16} xxl={14}>
                    <Pagination
                        className='cvat-tasks-pagination'
                        onChange={onSwitchPage}
                        total={numberOfTasks}
                        pageSize={10}
                        current={currentPage}
                        showQuickJumper
                    />
                </Col>
            </Row>
            <ModelRunnerModalContainer />
        </>
    );
}
